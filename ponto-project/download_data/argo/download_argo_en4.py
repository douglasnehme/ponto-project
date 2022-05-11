# -*- coding: utf-8 -*-
# AUTOR: Douglas Medeiros Nehme
# PLACE: Rio de Janeiro - Brazil
# CONTACT: medeiros.douglas3@gmail.com
# CRIATION: may/2022
# OBJECTIVE: Download EN4 data

import os
import warnings
import subprocess

import xarray as xr
import pandas as pd

from dotenv import load_dotenv

load_dotenv('/home/douglas/Dropbox/profissional/ponto-project/ponto-project/ponto.input')

############################################
# CONFIG PARAMETERS AND GLOBAL VARIABLES ###
############################################
def get_argo_en4_global_files(
    dir2get,
    dir2save,
    start_time,
    end_time
):
    """
    
    """

    months = pd.date_range(
        start_time,
        end_time,
        freq='M'
    )

    if months.empty:
        months = pd.date_range(
            start_time,
            end_time,
            periods=1
        )

    unziped_files = list()

    for year in range(start_time.year, end_time.year+1):
        zip_filename = (
            'EN.4.2.2.profiles.g10.' +
            str(year) +
            '.zip'
        )
        en4_filepath = os.path.join(
            dir2get,
            zip_filename
        )
        local_filepath = os.path.join(
            dir2save,
            zip_filename
        )
        months2unzip = months[
            months.year == year
        ]
        months2unzip = list(
            months2unzip.strftime('%Y%m')
        )
        subprocess.run([
            'wget',
            '--quiet',
            '--https-only',
            '-N',
            '-P',
            dir2save,
            en4_filepath
        ])
        for ym in months2unzip:
            file2unzip = (
                'EN.4.2.2.f.profiles.g10.' +
                '{0}.nc'.format(
                    ym
            ))
            subprocess.run([
                'unzip',
                '-q',
                '-o',
                '-d',
                dir2save,
                local_filepath,
                file2unzip,

            ])
            unziped_files.append(
                os.path.join(
                    dir2save,
                    file2unzip
            ))
        subprocess.run([
            'rm',
            local_filepath
        ])

    return unziped_files

# obsdir = os.environ[
#     'DATATYPE_DIR'
# ]
obsdir = '/home/douglas/Dropbox/profissional/ponto-project/data/argo'
en4_dir = (
    'https://www.metoffice.gov.uk/hadobs/' +
    'en4/data/en4-2-1/'
)
# Desired area
lonmin = float(
    os.environ[
      'LON_MIN'
])
lonmax = float(
    os.environ[
      'LON_MAX'
])
latmin = float(
    os.environ[
      'LAT_MIN'
])
latmax = float(
    os.environ[
      'LAT_MAX'
])
# Desired time
timemin = pd.to_datetime(
    os.environ[
        'DATETIME_MIN'],
    format='%d-%m-%Y %H:%M:%S'
)
timemax = pd.to_datetime(
    os.environ[
        'DATETIME_MAX'],
    format='%d-%m-%Y %H:%M:%S'
)
############################################
# IMPORTING AND MANIPULATING DATA ##########
############################################
argo_files = get_argo_en4_global_files(
    en4_dir,
    obsdir,
    timemin,
    timemax
)
nc = xr.open_mfdataset(
    argo_files,
    concat_dim='N_PROF',
    combine='nested',
    engine='netcdf4'
)
# Drop N_HISTORY dimension and associated
# variables because its shape (empty) caused
# a lot of trouble to use the where function
nc = nc.drop_dims(
    'N_HISTORY'
)
# Select data inside desired area and time
# and drop all outside of it
nc = nc.where(
    (nc.LONGITUDE >= lonmin) &
    (nc.LONGITUDE <= lonmax) &
    (nc.LATITUDE >= latmin) &
    (nc.LATITUDE <= latmax) &
    (nc.JULD >= timemin) &
    (nc.JULD <= timemax),
    drop=True
)
# Mask all data from other than ARGO project
# The symbol inside astype func means get
# just the first four values in the string
argo_mask = nc['PROJECT_NAME'].astype('|S4') == b'ARGO'

# Select just data from ARGO. Descided to
# mask the dataset by N_PROF dimension
# because it is the PROJECT_NAME dim
nc = nc.sel(
    N_PROF = argo_mask
)
if nc['N_PROF'].size > 0:
    print((
        '>>>> Getting ARGO data from EN4' +
        ' for {0} profiles').format(
            nc['N_PROF'].size
    ))
    # Save file
    warnings.simplefilter(
        "ignore",
        category=xr.SerializationWarning
    )
    nc.to_netcdf(
        os.path.join(
            obsdir,
            'argo_en4.nc'
    ))
else:
    print((
        '>>>> Not available ARGO data' +
        ' from EN4 for the desired area ' +
        'and time'
    ))

# Delete global files
for file in argo_files:
    try:
        os.remove(
            file
        )
    except:
        print(
            "Error while deleting file : ",
            file
        )
