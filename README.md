This is the begining of the pyNetCDF Conversion toolbox.
this tool will create netCDF files (hopefully CF compliant) with various inputs:
- matfile
- python dictionary
- netCDF file (rename and restruture to meet input yamls)

# assumptions
The code requires inputs additonal to the data types listed above:
 * input variable yaml: this file contains input variable names and output netCDF variable names with associate attributes.
    1. can use attributes to utilize netCDF compression capability
    2. can use significant digits to combine with that
    3. can assign data types 
        - strings (S1, S2, S4) 
        - (f1, f2, f4) for floats
        - (i1, i2, i4) for integers
        - (u1, u2, u4) for unsigned integers 
 * global metaData yaml; this holds all of the global netCDF metaData  
     
# start with CHL 
this is built off of USACE ERDC CHL models and observation data from the FRF.

# CF conventions
there are attributes that need to be included. It's  unclear if at this point we require metadata input yamls to be  
# UGRID
unstructured grid conventions
