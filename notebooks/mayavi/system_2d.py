import sys
import os
# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
os.environ['ETS_TOOLKIT'] = 'qt4'
# print os.getenv("ETS_TOOLKIT")
from mayavi import mlab
import mayavi
import sys
import matplotlib
from matplotlib.cm import datad, get_cmap
import numpy as np
from tvtk.api import tvtk
from mayavi.filters.user_defined import UserDefined

# -----------------------------------------------------------------------------

# Define and apply a UserDefined:CellCenters filter
CellCenter = UserDefined(filter=tvtk.CellCenters())

# -----------------------------------------------------------------------------

fig = mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(1500, 800))

# Read the last file from the base directory
base_dir = '../fidimag_2D_D2d_vtks/'
data = mlab.pipeline.open(base_dir + os.listdir(base_dir)[-1])

vtres = mlab.pipeline.threshold(data)
try:
    vtres.lower_threshold = 0.01
except:
    print('No points with zero vector norm')
# Extract vec comp and plot
vecomp = mlab.pipeline.extract_vector_components(vtres)
vecomp.component = 'z-component'  # Extract z-component of the data

# -----------------------------------------------------------------------------

# Extract cell data into Point Data. We can also use the cell centres

cell_centre = mlab.pipeline.user_defined(vecomp, filter=tvtk.CellCenters())
# cell_centre = mlab.pipeline.cell_to_point_data(vecomp)

# Draw glyphs within the clip filter region
glyphs = mlab.pipeline.glyph(cell_centre, mode='arrow')
glyphs.glyph.scale_mode = 'data_scaling_off'
glyphs.glyph.glyph.scale_factor = 5
glyphs.glyph.glyph_source.glyph_source.shaft_resolution = 40
glyphs.glyph.glyph_source.glyph_source.tip_resolution = 40
glyphs.glyph.glyph_source.glyph_source.tip_length = 0.4
glyphs.glyph.glyph_source.glyph_source.shaft_radius = 0.05
glyphs.glyph.glyph_source.glyph_source.tip_radius = 0.15
glyphs.glyph.mask_input_points = True
glyphs.glyph.mask_points.progress = 1.0
glyphs.glyph.mask_points.random_mode = False
glyphs.glyph.mask_points.on_ratio = 3
glyphs.parent.scalar_lut_manager.lut_mode = 'black-white'
# glyphs.parent.scalar_lut_manager.reverse_lut = True

# Surface with z as colormap
surf = mlab.pipeline.surface(vecomp, vmax=1, vmin=-1,
                             colormap='RdYlBu'
                             )
surf.actor.property.interpolation = 'flat'
surf.actor.property.opacity = 0.8

mlab.view(elevation=0, azimuth=0)

# Set the view (coordinates from Mayavi GUI)
fig.scene.camera.position = [99.32360796969633, -60.445450671671466, 81.08313678722261]
fig.scene.camera.focal_point = [50.48816838497997, 48.83956574747153, -6.895403097636284]
fig.scene.camera.view_angle = 30.0
fig.scene.camera.view_up = [-0.22675264287103733, 0.547259999733377, 0.8056610525790756]
fig.scene.camera.clipping_range = [34.57508169251493, 284.1085839216215]
fig.scene.camera.compute_view_plane_normal()
fig.scene.render()

mlab.savefig('system_2d.png')

mlab.show()
