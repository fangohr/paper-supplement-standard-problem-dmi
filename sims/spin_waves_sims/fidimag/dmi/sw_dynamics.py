from __future__ import print_function

import numpy as np
import shutil

from fidimag.micro import Sim
from fidimag.common import CuboidMesh
from fidimag.micro import UniformExchange, Demag, DMI, UniaxialAnisotropy
from fidimag.micro import Zeeman, TimeZeeman
import fidimag.common.constant as C


def exponential_damping(r, alpha, xmin, xmax, width_x, ymin, ymax, width_y):
    ya = ymin + width_y
    yb = ymax - width_y

    xa = xmin + width_x
    xb = xmax - width_x

    # if r[1] <= ya:
    #     return np.exp((ymin - r[1]) *
    #                   np.log(alpha) / (ymin - ya))
    # if r[1] >= yb:
    #     return np.exp((ymax - r[1]) *
    #                   np.log(alpha) / (ymax - yb))
    if r[0] <= xa:
        return np.exp((xmin - r[0]) *
                      np.log(alpha) / (xmin - xa))
    if r[0] >= xb:
        return np.exp((xmax - r[0]) *
                      np.log(alpha) / (xmax - xb))
    else:
        return alpha

# -----------------------------------------------------------------------------

ALPHA = 0.01
GAMMA = 2.21e5    # Hz / T
A = 13e-12        # J * m**-1
D = 3e-3          # J * m**-2
Ku = 0e6          # J * m**-3
Ms = 0.86e6       # A / m
B0 = 0.4          # T
EXC_FIELD = 0.04  # T
CUTOFF_F = 60e9

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

centre_x = (mesh.coordinates[:, 0].max()
            + mesh.coordinates[:, 0].min()) * 0.5 + mesh.coordinates[:, 0].min()
centre_y = (mesh.coordinates[:, 1].max()
            + mesh.coordinates[:, 1].min()) * 0.5 + mesh.coordinates[:, 1].min()
centre_z = 0.5

# -----------------------------------------------------------------------------

sim = Sim(mesh, name='dynamics')
sim.set_m(np.load('initial_state.npy'))

# -----------------------------------------------------------------------------

sim.Ms = Ms
sim.add(UniformExchange(A))
sim.add(Demag())
# sim.add(UniaxialAnisotropy(Ku, (0, 0, 1)))

# Periodic DMI
sim.add(DMI(D, dmi_type='interfacial'))

# External field along the stripe length
sim.add(Zeeman((0, B0 / mu0, 0)), save_field=True)


# -----------------------------------------------------------------------------
# Dynamics


def spatial_sinc_field(r, x0, y0, z0, h0):
    # x, y, z = pos[0], pos[1], pos[2]
    # h = h0 * (np.sinc(kc * (x - x0)) * np.sinc(kc * (y - y0))
    #           * np.sinc(kc * (z - z0))
    #           )
    if np.abs(r[0] - x0) <= 2:
        return (h0, 0, 0)
    else:
        return (0, 0, 0)

# cut-off frequency
f = CUTOFF_F
# We will delay the sinc pulse peak in 50 ps
t0 = 50 * 1e-12
# units in nm
h0 = (EXC_FIELD * B0) / mu0

sim.add(TimeZeeman(lambda r: spatial_sinc_field(r,
                                                centre_x,
                                                centre_y,
                                                centre_z,
                                                h0),
                   lambda t: np.sinc(2 * f * (t - t0))
                   ),
        save_field=True
        )

# -----------------------------------------------------------------------------

# sim.driver.alpha = lambda r: exponential_damping(r, ALPHA,
#                                                  0, 3000, 20,
#                                                  0, 200, 20)
sim.driver.alpha = ALPHA
sim.driver.gamma = GAMMA
# sim.driver.set_tols(rtol=1e-8, atol=1e-8)

times = np.arange(4000) * 1e-12
for t in times:
    print('t = {}'.format(t))
    sim.driver.run_until(t)
    # sim.save_vtk()
    sim.save_m()
