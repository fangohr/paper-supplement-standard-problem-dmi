import numpy as np

from finmag import Simulation as Sim
from finmag.energies import Exchange, Demag, DMI, Zeeman
from finmag.energies import UniaxialAnisotropy
from finmag.util.consts import mu0

import os, shutil
import dolfin as df

# Info
# from finmag.util.helpers import set_logging_level
# set_logging_level("INFO")
# set_logging_level("DEBUG")

# Geometries
from finmag.util.mesh_templates import Nanodisk


# MESH ------------------------------------------------------------------------

mesh_file = 'mesh/nanodisk.xml.gz'
if os.path.exists(mesh_file):
    mesh = df.Mesh(mesh_file)
else:
    mesh = Nanodisk(d=100, h=2,
                    center=(0, 0, 0),
                    valign='bottom',
                    name='nanodisk'
                    ).create_mesh(maxh=2,
                                  save_result=True,
                                  filename='nanodisk', directory='mesh',
                                  )


# Simulation and energies -----------------------------------------------------

# Bulk
A = 13e-12
D = 3e-3
Ms = 0.86e6
Ku = 0.4e6

sim = Sim(mesh, Ms=Ms, unit_length=1e-9, name="nanodisk_T")


def m_init(pos):
    x, y = np.array(pos)[:2]
    if (x ** 2 + y ** 2) ** 0.5 < 25:
        return (0, 0.1, 1)
    else:
        return (0, 0.1, -1)

sim.set_m(m_init)

# -----------------------------------------------------------------------------

# Exchange Energy
sim.add(Exchange(A))
# DMI
sim.add(DMI(D, dmi_type='bulk'))
# Uniaxial Anisotropy
sim.add(UniaxialAnisotropy(Ku, (0, 0, 1), name='Ku'))

# -----------------------------------------------------------------------------

sim.set_tol(1e-8, 1e-8)
sim.llg.presession = False
sim.alpha = 0.9

if not os.path.exists('vtks'):
    # shutil.rmtree('vtks')
    os.mkdir('vtks')

sim.relax(stopping_dmdt=0.01)
sim.save_vtk(filename='vtks/nanodisk_T.pvd', overwrite=True)
sim.save_field('m', 'nanodisk_T.npy', overwrite=True)

# Extract data
r_diam = np.linspace(-49.99, 49.99, 100)
data = np.zeros((len(r_diam), 4))

for i, r in enumerate(r_diam):
    data[i][0] = r
    data[i][1:] = sim.m_field.f((r, 0, 1))

np.savetxt('nanodisk_T_skyrmion.dat', data)

# Skyrmion radius
import scipy.optimize
r_sk = scipy.optimize.brentq(lambda r: sim.m_field.f((r, 0, 1))[2], 0, 49)
print(r_sk)

# Extract the radial component at r=r_sk
phi_ring = np.linspace(0, 2 * np.pi, 100)
data_mr = np.zeros((len(phi_ring), 2))
for i, phi in enumerate(phi_ring):
    x = r_sk * np.cos(phi)
    y = r_sk * np.sin(phi)

    mx, my, mz = sim.m_field.f((x, y, 1))

    mr = mx * np.cos(phi) + my * np.sin(phi)

    data_mr[i][0] = phi
    data_mr[i][1] = mr

np.savetxt('nanodisk_T_phi_mr_rsk.dat', data)
