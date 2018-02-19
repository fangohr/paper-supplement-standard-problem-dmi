from __future__ import print_function

import argparse
import numpy as np
from fidimag.micro import Sim
from fidimag.common import CuboidMesh
from os import listdir
import re

# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate data from NPY files')

parser.add_argument('--initial_state',
                    help='Path to the NPY file with the initial state',
                    default='InitialMagnetization.omf')

parser.add_argument('--mesh_lengths',
                    help='Cuboid mesh lengths in XYZ directions: '
                    'lx ly lz',
                    type=float, nargs=3)

parser.add_argument('--mesh_discretisation',
                    help='Cuboid mesh discretisation in XYZ directions: '
                    'dx dy dz',
                    type=float, nargs=3)

parser.add_argument('--npys_path',
                    help='Path to the folder with the NPY files',
                    default='unnamed_npys/')

parser.add_argument('--out_name',
                    help='Append this name to the data_mi file name',
                    default='')

# Parser arguments
args = parser.parse_args()

# -----------------------------------------------------------------------------

mu0 = 4 * np.pi * 1e-7

# Create simulation -----------------------------------------------------------
lx, ly, lz = args.mesh_lengths
dx, dy, dz = args.mesh_discretisation
nx, ny, nz = int(lx / dx), int(ly / dy), int(lz / dz)
print('Number of elements:', nx, ny, nz)

mesh = CuboidMesh(nx=nx, ny=ny, nz=nz,
                  dx=dx, dy=dy, dz=dz,
                  unit_length=1e-9
                  )
sim = Sim(mesh)
# We will get the spin components from the spins at the middle and across
# the sample length (in the X direction)
mask = mesh.coordinates[:, 1] == mesh.coordinates[:, 1][nx * int(ny * 0.5)]

# -----------------------------------------------------------------------------
# Load files from every time step
basedir = args.npys_path
if not basedir.endswith('/'):
    basedir += '/'
file_list = sorted(listdir(basedir),
                   key=lambda f: int(re.search(r'[0-9]+', f).group(0)))
print('Processing {} files'.format(len(file_list)))

# -----------------------------------------------------------------------------

# Create the arrays to store the data: every row is a time step
# Every column is a spin at the middle and across the sample (we get them
# masking the matrix with the spins)
data_mx = np.zeros((len(file_list), len(mask[mask])))
data_my = np.zeros((len(file_list), len(mask[mask])))
data_mz = np.zeros((len(file_list), len(mask[mask])))

# Magnetisation at t=0
sim.set_m(np.load(args.initial_state))
m0 = np.copy(sim.spin.reshape(-1, 3))

# For every file, compute the dynamic component (substract the static
# part from the initial state) and store it at one row
for i, _file in enumerate(file_list):
    tmp = np.load(basedir + _file)
    sim.set_m(tmp)

    m = np.copy(sim.spin.reshape(-1, 3))

    data_mx[i] = m[:, 0][mask] - m0[:, 0][mask]
    data_my[i] = m[:, 1][mask] - m0[:, 1][mask]
    data_mz[i] = m[:, 2][mask] - m0[:, 2][mask]

# Save the data and the x coordinates -----------------------------------------
# (it doesn't matter if the x coordinates are obtained at the middle or at the
# first row in the mesh, since the sample is rectangular)
if args.out_name:
    out_name = '_' + args.out_name
else:
    out_name = ''

np.savetxt('mesh_x-coordinates{}.dat'.format(args.out_name),
           mesh.coordinates[:, 0][mask])
np.savetxt('datafile_mx{}.dat'.format(args.out_name), data_mx)
np.savetxt('datafile_my{}.dat'.format(args.out_name), data_my)
np.savetxt('datafile_mz{}.dat'.format(args.out_name), data_mz)
