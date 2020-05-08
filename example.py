import py2netCDF as p2nc
import pickle, gridded
import netCDF4 as nc

# inputFile = "/home/spike/cmtb/data/waveModels/ww3/base/2018-03-02T000000Z/ww3.201803.nc"
varYaml = "/home/spike/repos/makeNetCDF/Station_Directional_Wave_var.yml"
globalYaml = "/home/spike/repos/makeNetCDF/Station_globalmeta.yml"
#
# with open('mesh.pickle', 'rb') as fid:
#     meshData = pickle.load(fid)
#
# p2nc.ncFile2ncFile(inputFile=inputFile, globalYaml=globalYaml, varYaml=varYaml, meshData=meshData)
# # Store data (serialize)
#
# ugridFile = "/home/spike/repos/makeNetCDF/ww3.201803_spec.ncfile"
# ugf = gridded.Dataset(ugridFile)
#
# nc = nc.Dataset(ugridFile)
#
# # need to convert to zero-indexing
# nodes = nc.variables['nodes'][:] - 1
# faces = nc.variables['E3T'][:, :3] - 1
#
# # make the grid
# # gridded.grids.Grid_U
# grid = gridded.grids.Grid_U(nodes=meshData['points'],
#                             faces=faces,
#                             )

######### load process ww3 spec files #######3
import sys
sys.path.append('/home/spike/repos')
from testbedutils import waveLib
import py2netCDF as p2nc
import numpy as np
fname = '/home/spike/repos/makeNetCDF/ww3.201803_spec.nc'
ncfile = nc.Dataset(fname)
idxSorted = np.argsort(ncfile['direction'][:])
dWEDout = ncfile['efth'][:, :, :, idxSorted]

for ss, station in enumerate(nc.chartostring(ncfile['station_name'][:])):
    stats = waveLib.waveStat(dWEDout[:,1],frqbins=ncfile['frequency'][:], dirbins=ncfile['direction'][:])
    out = {'waveHs': stats['Hm0'],
           'time': nc.date2num(nc.num2date(ncfile['time'][:], ncfile['time'].units), 'seconds since 1970-01-01'),
           'waveTm': stats['Tm'],
           'waveDm': stats['Dm'],
           'waveTp': stats['Tp'],
           'waterLevel': np.ones_like(stats['Hm0']) * -999,
           'windSpeed': ncfile['wnd'][:, ss],
           'windDirection': ncfile['wnddir'][:, ss],
           'currentSpeed': ncfile['cur'][:, ss],
           'currentDirection': ncfile['curdir'][:, ss],
           'flags': np.ones_like(stats['Hm0']) * -999,
           'longitude': ncfile['longitude'][0, ss],  # assume static location
           'latitude': ncfile['latitude'][0, ss],    # assume static location
           'waveDirectionBins': ncfile['direction'][:],
           'waveFrequency': ncfile['frequency'][:],
           'directionalWaveEnergyDensity': dWEDout[:,ss],
           'station_name': station
    }
    p2nc.makenc_generic('test.nc', globalYaml, varYaml, out)