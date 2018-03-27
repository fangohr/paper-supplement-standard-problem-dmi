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

# Read the simulation file
base_file = '../../sims/finmag/3D/vtks/m000001.vtu'
data = mlab.pipeline.open(base_file)

# Extract vec comp and plot
vecomp = mlab.pipeline.extract_vector_components(data)
vecomp.component = 'z-component'  # Extract z-component of the data

# -----------------------------------------------------------------------------

dc = mlab.pipeline.data_set_clipper(vecomp)
dc._transform.matrix.__setstate__({'elements': [0.6486929348073014, 0.0, 0.0, 52.41333972491739, 0.0, 0.68495045321519, 0.0, -54.67190868447851, 0.0, 0.0, 2.497856901910694, -22.880355891164257, 0.0, 0.0, 0.0, 1.0]})
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
glyphs.glyph.mask_input_points = True
glyphs.glyph.mask_points.progress = 1.0
glyphs.glyph.mask_points.random_mode = False
glyphs.glyph.mask_points.on_ratio = 2
glyphs.parent.scalar_lut_manager.lut_mode = 'black-white'

# Clip data to draw a surface
dc2 = mlab.pipeline.data_set_clipper(vecomp)
dc2._transform.matrix.__setstate__({'elements': [0.6486929348073014, 0.0, 0.0, 52.41333972491739, 0.0, 0.68495045321519, 0.0, -54.67190868447851, 0.0, 0.0, 2.497856901910694, -22.880355891164257, 0.0, 0.0, 0.0, 1.0]})
dc2.widget.widget.set_transform(dc2._transform)
dc2.widget.update_implicit_function()
dc2.render()
dc2.widget.widget.enabled = False
# vecomp.filter.inside_out = True

# Surface with z as colormap
surf = mlab.pipeline.surface(dc2, vmax=1, vmin=-1,
                             colormap='RdYlBu'
                             )
surf.actor.property.interpolation = 'flat'

# surface with wire showing the FE tetrahedra
surf = mlab.pipeline.surface(dc2, vmax=1, vmin=-1,
                             colormap='RdYlBu'
                             )
surf.actor.property.representation = 'wireframe'


mlab.view(elevation=0, azimuth=0)

# Set the view (coordinates from Mayavi GUI)
fig.scene.camera.position = [136.73338488323722, -155.07821189742828, 140.05918124152356]
fig.scene.camera.focal_point = [0.4209890027534655, -0.405654124817314, -2.80443285291378]
fig.scene.camera.view_angle = 30.0
fig.scene.camera.view_up = [-0.3993624094347138, 0.4068782082277992, 0.8215593646230537]
fig.scene.camera.clipping_range = [21.185478265041723, 538.9625363718424]
fig.scene.camera.compute_view_plane_normal()
fig.scene.render()

mlab.savefig('system_3d_cylinder_finmag.png')

mlab.show()
