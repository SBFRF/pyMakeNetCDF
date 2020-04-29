import py2netCDF as p2nc

inputFile = "/home/spike/cmtb/data/waveModels/ww3/base/2018-03-02T000000Z/2018-03-02T000000Z.nc"
varYaml = "/home/spike/repos/makeNetCDF/Field_var.yml"
globalYaml  = "/home/spike/repos/makeNetCDF/field_globalmeta.yml"

p2nc.ncFile2ncFile(inputFile=inputFile, globalYaml=globalYaml, varYaml=varYaml)
