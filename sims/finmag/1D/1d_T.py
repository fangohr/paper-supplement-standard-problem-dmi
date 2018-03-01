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
from finmag.util.meshes import line_mesh


# MESH ------------------------------------------------------------------------

mesh = line_mesh(np.linspace(0, 100, 21))


# Simulation and energies -----------------------------------------------------

# Bulk
A = 13e-12
D = 3e-3
Ms = 0.86e6
Ku = 0.4e6
initial_sk_diam = 10

sim = Sim(mesh, Ms=Ms, unit_length=1e-9, name="1d_T")
sim.set_m((0, 0.1, 0.9))

# -----------------------------------------------------------------------------

# Exchange Energy
sim.add(Exchange(A))
# DMI
sim.add(DMI(D, dmi_type='bulk'))
# Uniaxial Anisotropy
sim.add(UniaxialAnisotropy(Ku, (0, 0, 1), name='Ku'))

# -----------------------------------------------------------------------------

sim.do_precession = False
sim.alpha = 0.9

if not os.path.exists('vtks'):
    # shutil.rmtree('vtks')
    os.mkdir('vtks')

sim.relax()
sim.save_vtk(filename='vtks/1d_T.pvd', overwrite=True)
sim.save_field('m', '1d_T.npy', overwrite=True)

xs = sim.mesh.coordinates()
# Data in format: x mx my mz
data = np.zeros((len(xs), 4))
for i, x in enumerate(xs):
    data[i][0] = x
    data[i][1:] = sim.m_field.f(x)

np.savetxt('1d_T.dat', data)
