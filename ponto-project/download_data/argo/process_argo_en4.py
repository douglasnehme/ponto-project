# -*- coding: utf-8 -*-
# AUTOR: Douglas Medeiros Nehme
# PLACE: Rio de Janeiro - Brazil
# CONTACT: medeiros.douglas3@gmail.com
# CRIATION: mar/2021
# OBJECTIVE: Process EN4 data

import os
import glob

import xarray as xr

from numpy import array
from datetime import datetime

start = datetime.now().replace(microsecond=0)
############################################
# CONFIG PARAMETERS AND GLOBAL VARIABLES ###
############################################
obsdir = os.getenv(
    'DataDir')

fname = 'EN.4.2.1.f.profiles.g10.20*.nc'

# Desired space and time
xmin = -46.50
xmax = -37.40
ymin = -27.35
ymax = -18.90
tmin = datetime(2019, 12,  2,  0,  0,  0)
tmax = datetime(2020, 12, 31, 23, 59, 59)

############################################
# IMPORTING AND MANIPULATING DATA ##########
############################################
# Open multi-files
nc = xr.open_mfdataset(
    os.path.join(
        obsdir,
        fname),
    concat_dim='N_PROF',
    combine='nested')

# Drop N_HISTORY dimension and associated
# variables because its shape (empty) caused
# a lot of trouble to use the where function
nc = nc.drop_dims(
    'N_HISTORY')

# Format tmin and tmax to it be understood
# by where function
tmin = array(
    [tmin],
    dtype='datetime64[ns]')
tmax = array(
    [tmax],
    dtype='datetime64[ns]')

# Select data inside desired area and time
# and drop all outside of it
nc = nc.where(
    (nc.LONGITUDE > xmin) &
    (nc.LONGITUDE < xmax) &
    (nc.LATITUDE > ymin) &
    (nc.LATITUDE < ymax) &
    (nc.JULD > tmin) &
    (nc.JULD < tmax),
    drop=True)

# Select just the profiles that pass on
# quality control
nc = nc.where(
    (nc.POSITION_QC == b'1') &
    (nc.PROFILE_POTM_QC == b'1') &
    (nc.PROFILE_PSAL_QC == b'1'),
    drop=True)

# Select, in each profile, just the levels
# that temperature data pass on quality
# control
nc['POTM_CORRECTED'] = nc.POTM_CORRECTED.where(
    nc.POTM_CORRECTED_QC == b'1')
nc['PSAL_CORRECTED'] = nc.PSAL_CORRECTED.where(
    nc.PSAL_CORRECTED_QC == b'1')

# Save processed file
nc.to_netcdf(
    os.path.join(
        obsdir,
        (fname[:-6] +
        'CronosHindcast.nc')))

# List original unprocessed EN4 files
fileList = glob.glob(
    os.path.join(
        obsdir,
        fname))

# Delete above list of unprocessed files
for filePath in fileList:
    try:
        os.remove(filePath)
    except:
        print(
            "Error while deleting file : ",
            filePath)

stop = datetime.now().replace(microsecond=0)
print(
    'Time taken to execute program:' +
    '{}'.format(stop - start))
