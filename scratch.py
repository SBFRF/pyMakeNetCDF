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
ncfile = nc.Dataset(fname)

with open('mesh.pickle', 'rb') as fid:
    meshdata = pickle.load(fid)
    
# start index = 1
nNodes = 108403  #?
nFaces = 216804  #?

connectivity = np.ma.masked_all((meshdata['cell_data']['triangle'][-1,0], 3), dtype=int)
faceNum = np.append(meshdata['cell_data']['vertex'][:, 0], meshdata['cell_data']['triangle'][:, 0])
connectivity[:meshdata['cell_data']['vertex'][:,-1].shape[0], 0] = meshdata['cell_data']['vertex'][:,-1]
connectivity[-meshdata['cell_data']['triangle'].shape[0]:, -3:] = meshdata['cell_data']['triangle'][:,-3:]
# connectivity[-meshdata['cell_data']['triangle'].shape[0]:, 1] = meshdata['cell_data']['triangle'][:,4]
nodeNum = np.arange(meshdata['points'].shape[0], dtype=int)

out = {'time':  nc.date2num(nc.num2date(ncfile['time'][:], ncfile['time'].units), 'seconds since 1970-01-01'),
       'latitude': ncfile['latitude'][:],
       'longitude': ncfile['longitude'][:],
       'meshName': -999,
       'connectivity': connectivity,
       'three': np.ones((3)) * -999,
       'faces': faceNum -1, # set to zero index
       'nodes': nodeNum,
       'waveHs': ncfile['hs'][:],
       }

p2nc.makenc_generic('test.nc', globalYaml='field_globalmeta.yml', varYaml='Field_var.yml', data=out)
# ug = pug.UGrid.from_ncfile('test.nc')
# ug.build_edges()
# print('There are {} x {} nodes'.format(*ug.nodes.shape))
# print('There are {} x {} edges'.format(*ug.edges.shape))
# print('There are {} x {} faces'.format(*ug.faces.shape))
# print('First 5 elements of the connectivity array are:\n\n{}'.format(ug.faces[:5]))


## now check my file to make sure it is compliant
# Load all available checker classes
check_suite = CheckSuite()
check_suite.load_all_available_checkers()

path = 'test.nc'
checker_names = ['cf', 'acdd', 'UGRID']
verbose = 0
criteria = 'normal'
output_filename = 'report.json'
output_format = 'json'
return_value, errors = ComplianceChecker.run_checker(path,
                                                     checker_names,
                                                     verbose,
                                                     criteria,
                                                     output_filename=output_filename,
                                                     output_format=output_format)

# Open the JSON output and get the compliance scores
with open(output_filename, 'r') as fp:
    cc_data = json.load(fp)
    scored = cc_data[cc_test[0]]['scored_points']
    possible = cc_data[cc_test[0]]['possible_points']
    log.debug('CC Scored {} out of {} possible points'.format(scored, possible))





psy.plot.mapplot('http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_GOM3_FORECAST.nc')
psy.plot.mapplot('http://geoport.usgs.esipfed.org/thredds/dodsC/estofs/atlantic')
psy.plot.mapplot('test.nc')

lon = ug.nodes[:, 0]
lat = ug.nodes[:, 1]
edges = ug.edges
faces = ug.faces
triang = tri.Triangulation(lon, lat, triangles=faces)
def make_map(projection=ccrs.PlateCarree()):
    fig, ax = plt.subplots(figsize=(8, 6),
                           subplot_kw=dict(projection=projection))
    ax.coastlines(resolution='50m', zorder=1)
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax