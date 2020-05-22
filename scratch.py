import netCDF4 as nc
import pickle
import numpy as np
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib import pyplot as plt
import json
import pyugrid as pug
import psyplot.project as psy
from compliance_checker.runner import ComplianceChecker, CheckSuite
import py2netCDF as p2nc
from matplotlib import tri
# now work with the spatial output
fname = 'ww3.201803.nc'
fieldNc = nc.Dataset(fname)

with open('mesh.pickle', 'rb') as fid:
    meshdata = pickle.load(fid)
    
# start index = 1

# faceNum = meshdata['cell_data']['triangle'][:, 4]
# # connectivity = np.ma.masked_all((np.size(faceNum), 3), dtype=int)
# # connectivity[:, :] = meshdata['cell_data']['triangle'][:,-3:]
# nodeNum = np.arange(fieldNc.dimensions['node'].size, dtype=int)

out = {'time':            nc.date2num(nc.num2date(fieldNc['time'][:], fieldNc['time'].units), 'seconds since 1970-01-01'),
       'latitude':        fieldNc['latitude'][:],
       'longitude':       fieldNc['longitude'][:],
       'meshName':        -999,
       'connectivity':    fieldNc['tri'][:],
       'three':           np.ones((3)) * -999,
       'nfaces':          np.arange(fieldNc['tri'].shape[0], dtype=int),
       'nnodes':          np.arange(fieldNc.dimensions['node'].size, dtype=int),
       'xFRF':            np.ones_like(fieldNc['latitude'][:]) * -999,
       'yFRF':            np.ones_like(fieldNc['latitude'][:]) * -999,
       'waveHs':          np.ma.masked_array(fieldNc['hs'][:], mask=fieldNc['hs']._FillValue),
       'bathymetry':      meshdata['points'][:,2],  # doesn't need to be expanded into time dimension
       'waveTm':          fieldNc['t02'][:],
       'waveDm':          fieldNc['dir'][:],
       'dynamicTimeStep': fieldNc['dtd'][:] * 60,  # convert to seconds
       'mapStatus':       fieldNc['MAPSTA'][:]}

p2nc.makenc_generic('test.nc', globalYaml='field_globalmeta.yml', varYaml='Field_var.yml', data=out)

#
# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# from numpy import array
# from numpy import max
# # lonLowerLeft =
# # lonUpperRight =
# # latLowerLeft =
# # latUpperRight =
# lat_0 = np.median(fieldNc['latitude'][:])
# lon_0 = np.median(fieldNc['longitude'][:])
# waves = fieldNc['waveHs'][10]
# map = Basemap(resolution='h', area_thresh=10, lon_0=lon_0, lat_0=lat_0 )#llcrnrlon=lonLowerLeft, llcrnrlat=latLowerLeft,
# map.contourf(fieldNc['longitude'][:], fieldNc['latitude'][:], fieldNc['waveHs'][0], tri=True)
# urcrnrlat=latUpperRight,
              # urcrnrlon=lonUpperRight)



## now check my file to make sure it is compliant
# Load all available checker classes
# check_suite = CheckSuite()
# check_suite.load_all_available_checkers()

# path = 'test.nc'
# checker_names = ['UGRID']
# verbose = 0
# criteria = 'normal'
# output_filename = 'report.json'
# output_format = 'json'
# return_value, errors = ComplianceChecker.run_checker(path,
#                                                      checker_names,
#                                                      verbose,
#                                                      criteria,
#                                                      output_filename=output_filename,
#                                                      output_format=output_format)
#
# # Open the JSON output and get the compliance scores
# with open(output_filename, 'r') as fp:
#     cc_data = json.load(fp)
#     scored = cc_data[checker_names[0]]['scored_points']
#     possible = cc_data[checker_names[0]]['possible_points']
    # log.debug('CC Scored {} out of {} possible points'.format(scored, possible))





# psy.plot.mapplot('http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_GOM3_FORECAST.nc')
# psy.plot.mapplot('http://geoport.usgs.esipfed.org/thredds/dodsC/estofs/atlantic')
# psy.plot.mapplot('test.nc')



# ug = pug.UGrid.from_ncfile('test.nc')
# ug.build_edges()
# print('There are {} x {} nodes'.format(*ug.nodes.shape))
# print('There are {} x {} edges'.format(*ug.edges.shape))
# print('There are {} x {} faces'.format(*ug.faces.shape))
# print('First 5 elements of the connectivity array are:\n\n{}'.format(ug.faces[:5]))
#
# lon = ug.nodes[:, 0]
# lat = ug.nodes[:, 1]
# edges = ug.edges
# faces = ug.faces

# def make_map(projection=ccrs.PlateCarree()):
#     fig, ax = plt.subplots(figsize=(8, 6),
#                            subplot_kw=dict(projection=projection))
#     ax.coastlines(resolution='10m', zorder=1)
#     # ax.b()
#     # ax.set_extent([30,-70,-30,70])
#     #
#     gl = ax.gridlines(draw_labels=True)
#     # gl.xlabels_top = gl.ylabels_right = False
#     gl.xformatter = LONGITUDE_FORMATTER
#     gl.yformatter = LATITUDE_FORMATTER
#     return fig, ax
#
# # fig, ax = make_map()

from mpl_toolkits.axes_grid1 import make_axes_locatable
#################### inputs
# lon, lat, Value, bathy
###################
fieldNc = nc.Dataset('test.nc')
lon, lat = fieldNc['longitude'][:], fieldNc['latitude'][:]
value = fieldNc['waveHs'][-1, :]
bathy = fieldNc['bathymetry'][0]
title = fieldNc['waveHs'].short_name
axisLabel = title + ' [{}]'.format(fieldNc['waveHs'].units)
figsize = (16, 6)
outFname = 'test_plot.png'
######### pre process
triang = tri.Triangulation(lon, lat)

# take these from data or FRF locations
zoomBL = (-75.758986, 36.173927)
zoomTR = (-75.743879, 36.190276)
###########################
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=figsize, subplot_kw=dict(projection=ccrs.PlateCarree()))
####
axis = 0  # first subplot
ax[axis].coastlines(resolution='10m', zorder=1)
lines = ax[axis].triplot(triang, linestyle='-', lw=1, alpha=0.35, color='darkgray', zorder=1)
ax[axis].tricontour(triang, bathy, linestyles='dotted', colors='black', levels=[0, 1, 3.5, 5, 7])
ax[axis].set_extent([zoomTR[0], zoomBL[0], zoomBL[1], zoomTR[1]])
ax[axis].set_title('Mesh', fontsize=12)

####
axis = 1  #2nd subplot
ax[axis].coastlines(resolution='10m', zorder=1)
mappable = ax[axis].tripcolor(triang, value)
ax[axis].tricontour(triang, bathy, linestyles='dotted', colors='black', levels=[0, 1, 3.5, 5, 7])
ax[axis].set_extent([zoomTR[0], zoomBL[0], zoomBL[1], zoomTR[1]])
cbar = plt.colorbar(mappable, ax=ax[axis], fraction=0.046, pad=0.04)
cbar.set_label(axisLabel)
ax[axis].set_title('nearshore {0}'.format(title), fontsize=12)

####
axis = 2  #3nd subplot
ax[axis].coastlines(resolution='10m', zorder=1)
mappable = ax[axis].tripcolor(triang, value)
ax[axis].tricontour(triang, bathy, linestyles='dotted', colors='black', levels=[0, 5, 10, 15, 20])
cbar = plt.colorbar(mappable, ax=ax[axis], fraction=0.046, pad=0.04)
cbar.set_label(axisLabel)
ax[axis].set_title('nearshore {0}'.format(title), fontsize=12)

for axis in range(0, len(ax)):
    print(axis)
    gl = ax[axis].gridlines(draw_labels=True)
    gl.top_labels= gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

plt.tight_layout()
plt.savefig(outFname)
