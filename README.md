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
        - strings (S1, S2, S4, S8) 
        - (f1, f2, f4, f8) for floats
        - (i1, i2, i4, i8) for integers
        - (u1, u2, u4, u8) for unsigned integers 
 * global metaData yaml; this holds all of the global netCDF metaData  

# CF conventions
The dimensions are created based on CF conventions http://cfconventions.org/cf-conventions/cf-conventions.html#dimensions

see `example.py` for a working example converting Wave Watch 3 station output to individual netCDF files.

Check the issues page for areas of active development or contribution suggestions.

# acknowledgements
this work was built off of work originally developed by RPS ASA. 
