from __future__ import print_function

import numpy as np
import shutil

from fidimag.micro import Sim
from fidimag.common import CuboidMesh
from fidimag.micro import UniformExchange, Demag, DMI, UniaxialAnisotropy
from fidimag.micro import Zeeman, TimeZeeman
import fidimag.common.constant as C

# -----------------------------------------------------------------------------

mu0 = 4 * np.pi * 1e-7

lx = 2000
ly = 200
lz = 1

dx, dy, dz = 2, 2, 1
nx, ny, nz = int(lx / dx), int(ly / dy), 1

print('Number of elements:', nx, ny, nz)


mesh = CuboidMesh(nx=nx, ny=ny, nz=nz,
                  dx=dx, dy=dy, dz=dz,
                  unit_length=1e-9
                  )

centre_x = (np.max(mesh.coordinates[:, 0])
            + np.min(mesh.coordinates[:, 0])) * 0.5
centre_y = (np.max(mesh.coordinates[:, 1])
            + np.min(mesh.coordinates[:, 1])) * 0.5
centre_z = 0.5

# -----------------------------------------------------------------------------

sim = Sim(mesh)
sim.driver.gamma = 2.21e5
sim.set_m((0.1, 0.9, 0))

# -----------------------------------------------------------------------------

A = 13e-12    # J * m**-1
D = 3e-3        # J * m**-2
Ku = 0e6        # J * m**-3
Ms = 0.86e6    # A / m
B0 = 0.4       # T

sim.Ms = Ms
sim.add(UniformExchange(A))
sim.add(Demag())
# sim.add(UniaxialAnisotropy(Ku, (0, 0, 1)))

# Periodic DMI
sim.add(DMI(D, dmi_type='interfacial'))

# External field along the stripe length
sim.add(Zeeman((0, B0 / mu0, 0)), save_field=True)

# -----------------------------------------------------------------------------

# Relax the system first
sim.driver.alpha = 0.9
sim.driver.do_precession = False
sim.driver.relax(stopping_dmdt=0.01)
np.save('initial_state.npy', sim.spin)

# Remove automatically saved files
shutil.rmtree('unnamed_npys/')
shutil.rmtree('unnamed_vtks/')
shutil.move('unnamed.txt', 'relaxation.txt')
