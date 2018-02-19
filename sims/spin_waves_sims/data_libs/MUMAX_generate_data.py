from __future__ import print_function
import numpy as np
# import os
from os import listdir
import re
# import gc
# import sys
import pandas as pd
import argparse

# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Generate data from OVF files')

parser.add_argument('--initial_state',
                    help='Path to the OMF file with the initial state',
                    default='InitialMagnetization.ovf')

parser.add_argument('--ovfs_path',
                    help='Path to the folder with the OMF files',
                    default='ovfs/')

parser.add_argument('--out_name',
                    help='Append this name to the data_mi file name',
                    default='')

# Parser arguments
args = parser.parse_args()

# -----------------------------------------------------------------------------

mu0 = 4 * np.pi * 1e-7


# -----------------------------------------------------------------------------
# Load the files with the spin components

basedir = args.ovfs_path
if not basedir.endswith('/'):
    basedir += '/'

file_list = [_file for _file in listdir(basedir)
             if _file.startswith('m')]
file_list = sorted(file_list)

print('Processing {} files'.format(len(file_list)))

# -----------------------------------------------------------------------------
# Load the coordinates

coordinates = pd.read_csv(basedir + file_list[0], comment='#',
                          header=None, delim_whitespace=True)
coordinates = coordinates.as_matrix()[:, :3]

nx = len(np.unique(coordinates[:, 0]))
ny = len(np.unique(coordinates[:, 1]))

# -----------------------------------------------------------------------------

# Create the arrays to store the data: every row is a time step
# Every column is a spin at the middle and across the sample
data_mx = np.zeros((len(file_list), len(coordinates[:, 0])))
data_my = np.zeros((len(file_list), len(coordinates[:, 0])))
data_mz = np.zeros((len(file_list), len(coordinates[:, 0])))

# Static data -----------------------------------------------------------------

m = pd.read_csv(args.initial_state, comment='#',
                header=None, delim_whitespace=True)

data_mx0 = m.as_matrix()[:, 3]
data_my0 = m.as_matrix()[:, 4]
data_mz0 = m.as_matrix()[:, 5]

# -----------------------------------------------------------------------------

# For every file, compute the dynamic component (substract the static
# part from the initial state) and store it at one row
for i, _file in enumerate(file_list):
    # print(i)

    m = pd.read_csv(basedir + _file, comment='#',
                    header=None, delim_whitespace=True)
    m = m.as_matrix()
    data_mx[i] = m[:, 3] - data_mx0
    data_my[i] = m[:, 4] - data_my0
    data_mz[i] = m[:, 5] - data_mz0

# Save the data and the x coordinates -----------------------------------------
# (it doesn't matter if the x coordinates are obtained at the middle or at the
# first row in the mesh, since the sample is rectangular)

if args.out_name:
    out_name = '_' + args.out_name
else:
    out_name = ''

# Coordinates are saved in nm
np.savetxt('mesh_x-coordinates{}.dat'.format(args.out_name),
           coordinates[:, 0][:nx] * 1e9)
np.savetxt('datafile_mx{}.dat'.format(out_name), data_mx)
np.savetxt('datafile_my{}.dat'.format(out_name), data_my)
np.savetxt('datafile_mz{}.dat'.format(out_name), data_mz)
