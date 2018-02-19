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
base_dir = '../fidimag_3D_cyl_vtks/'
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

# Clip the data to cut a piece of the square. The matrix is computed
# directly from Mayavi
dc = mlab.pipeline.data_set_clipper(cell_centre)
# dc.filter.inside_out = True
dc._transform.matrix.__setstate__({'elements': [0.6731526899911355, 0.0, 0.0, 87.48127163850997, 0.0, 0.757190029581168, 0.0, -39.14921017615853, 0.0, 0.0, 1.3846567118448652, -1.951553470812339, 0.0, 0.0, 0.0, 1.0]})
dc.widget.widget.set_transform(dc._transform)
dc.widget.update_implicit_function()
dc.render()
dc.widget.widget.enabled = False

# Draw glyphs within the clip filter region
glyphs = mlab.pipeline.glyph(dc, mode='arrow')
glyphs.glyph.scale_mode = 'data_scaling_off'
glyphs.glyph.glyph.scale_factor = 3
glyphs.glyph.glyph_source.glyph_source.shaft_resolution = 20
glyphs.glyph.glyph_source.glyph_source.tip_resolution = 20
glyphs.glyph.glyph_source.glyph_source.tip_length = 0.4
glyphs.glyph.glyph_source.glyph_source.shaft_radius = 0.05
glyphs.glyph.glyph_source.glyph_source.tip_radius = 0.15
# glyphs.glyph.mask_input_points = True
# glyphs.glyph.mask_points.progress = 1.0
# glyphs.glyph.mask_points.random_mode = False
# glyphs.glyph.mask_points.on_ratio = 2
glyphs.parent.scalar_lut_manager.lut_mode = 'black-white'

# Clip data to draw a surface
vecomp = mlab.pipeline.data_set_clipper(vecomp)
vecomp._transform.matrix.__setstate__({'elements': [0.6795458491915533, 0.0, 0.0, 86.39959770788616, 0.0, 0.7624134151875754, 0.0, -39.22474554337004, 0.0, 0.0, 1.2205789063641583, -1.9707571225107472, 0.0, 0.0, 0.0, 1.0]})
vecomp.widget.widget.set_transform(vecomp._transform)
vecomp.widget.update_implicit_function()
vecomp.render()
vecomp.widget.widget.enabled = False
# vecomp.filter.inside_out = True

# Surface with z as colormap
surf = mlab.pipeline.surface(vecomp, vmax=1, vmin=-1,
                             colormap='RdYlBu'
                             )
surf.actor.property.interpolation = 'flat'


mlab.view(elevation=0, azimuth=0)

# Set the view (coordinates from Mayavi GUI)
fig.scene.camera.position = [225.79348206790564, -65.35463216386151, 152.22309264982135]
fig.scene.camera.focal_point = [89.481086187422022, 89.317925608749434, 9.359478555383852]
fig.scene.camera.view_angle = 30.0
fig.scene.camera.view_up = [-0.39936240943471379, 0.40687820822779919, 0.82155936462305368]
fig.scene.camera.clipping_range = [21.185478265041723, 538.96253637184236]
fig.scene.camera.compute_view_plane_normal()

mlab.savefig('system_3d_cylinder.png')

mlab.show()
