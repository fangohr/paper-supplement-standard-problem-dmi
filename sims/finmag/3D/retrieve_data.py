import numpy as np

from finmag import Simulation as Sim
from finmag.energies import Exchange, Demag, DMI, Zeeman
from finmag.util.consts import mu0

import os, shutil
import dolfin as df

import scipy.optimize

import finmag


# MESH ------------------------------------------------------------------------

mesh_file = 'mesh/nanocylinder.xml.gz'
mesh = df.Mesh(mesh_file)

# Simulation and energies -----------------------------------------------------

# Bulk
A = 8.78e-12
D = 1.58e-3
Ms = 3.84e5
B = 0.4
initial_sk_diam = 20

sim = Sim(mesh, Ms=Ms, unit_length=1e-9, name="unnamed")
sim.set_m(np.load('m_relaxed.npy'))


# -----------------------------------------------------------------------------
# Skyrmion radius vs z

sk_radius = {}
for i, z in enumerate(np.linspace(0, 21, 11)):
    # Skyrmion radius: m_z = 0
    rsk = scipy.optimize.brentq(lambda x: sim.m_field.f((x, 0, z))[2], 0, 50)
    sk_radius[z] = rsk
    print('At z = {:<5}, r_sk = {:.3f}'.format(z, rsk))

# -----------------------------------------------------------------------------
# Get the data at the center of the cylinder

data = {}

xs = np.linspace(0, 91.49, 100)
zs = [0, 10.5, 20.99]
for j, z_layer in enumerate(['bottom', 'center', 'top']):
    data[z_layer] = np.zeros((len(xs), 8))
    for i, x in enumerate(xs):

        xi, yi, zi = x, 0, zs[j]
        phi = np.arctan2(yi, xi)

        mx, my, mz = np.copy(sim.m_field.f((xi, yi, zi)))
        mphi = (-mx * np.sin(phi) + my * np.cos(phi))
        mr = (mx * np.cos(phi) + my * np.sin(phi))

        data[z_layer][i] = [xi, yi, zi, mx, my, mz, mr, mphi]

    np.savetxt('m_{}.dat'.format(z_layer), data[z_layer])

# -----------------------------------------------------------------------------
# Extract m components across the thickness

data_acrossz = {}
zs = np.linspace(0, 20.99, 11)
for j, x_pos in enumerate(['center', 'sk_rad', 'boundary']):
    xs = [0, sk_radius[0], 91.49]
    data_acrossz[x_pos] = np.zeros((len(zs), 8))
    for i, z in enumerate(zs):

        xi, yi, zi = xs[j], 0, z
        phi = np.arctan2(yi, xi)

        mx, my, mz = np.copy(sim.m_field.f((xi, yi, zi)))
        mphi = (-mx * np.sin(phi) + my * np.cos(phi))
        mr = (mx * np.cos(phi) + my * np.sin(phi))

        data_acrossz[x_pos][i] = [xi, yi, zi, mx, my, mz, mr, mphi]

    np.savetxt('m_across-z_{}.dat'.format(x_pos), data_acrossz[x_pos])


# Print mesh
print('Mesh\n')
print(finmag.util.meshes.mesh_info(mesh))
print(finmag.util.meshes.mesh_quality(mesh))
