This is the beginning of the pyNetCDF Conversion toolbox.
this tool will create netCDF files (hopefully CF compliant) with various inputs:
- matfile
- python dictionary
- netCDF file (rename and restructure to meet input ymls)

# assumptions
The code requires inputs additional to the data types listed above:
 * input variable yaml: this file contains input variable names and output netCDF variable names with associate attributes.
    1. can use attributes to utilize netCDF4 variable level compression using`least_significant_digit`
                                              and `comp_level` attributecompression capability
    2. can use significant digits to combine with that
    3. can assign data types for different precisions 
        - strings: 'S1' or 'c' (NC_CHAR) 
        - bytes: 'i1' or 'b' or 'B'(NC_BYTE)
        - unsigned bytes: 'u1' (NC_UBYTE)
        - shorts: 'i2' or 'h' or 's' (NC_SHORT), 
        - unsigned shorts: 'u2' (NC_USHORT)
        - integers: 'i4' or 'i' or 'l' (NC_INT), 'i8' (NC_INT64)
        - unsigned integers: 'u4' (NC_UINT), 'u8' (NC_UINT64)
        - floats: 'f4' or 'f' (NC_FLOAT), 'f8' or 'd' (NC_DOUBLE)`.
        
 * global metaData yaml; this holds all of the global netCDF metaData  

# CF conventions
The dimensions are created based on CF conventions http://cfconventions.org/cf-conventions/cf-conventions.html#dimensions

see `example.py` for a working example converting Wave Watch 3 station output to individual netCDF files.

Check the issues page for areas of active development or contribution suggestions.

# acknowledgements
this work was built off of work originally developed by RPS ASA. 
