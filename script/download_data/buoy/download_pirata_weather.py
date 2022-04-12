# -*- coding: utf-8 -*-
# AUTOR: Douglas Medeiros Nehme
# PLACE: Rio de Janeiro - Brazil
# CONTACT: medeiros.douglas3@gmail.com
# CRIATION: apr/2022
# OBJECTIVE: Download PIRATA buoy data for
#            desired area and time

import os
import subprocess

import pandas as pd
import ftputil as ftp

from dotenv import load_dotenv

load_dotenv('/home/douglas/Dropbox/profissional/ponto-project/ponto.input')

############################################
# SET SOME FUNCTIONS AND/OR VARIABLES ######
############################################
def spatial_filter(
    lonmin=-66.,
    lonmax=8.,
    latmin=-63.,
    latmax=21.,
    responsible='PIRATA'
    ):
    '''
    Select weather buoys in expanded South Atlantic by area and institution of responsability.

    For more details of the weather buoys' database access https://github.com/douglasnehme/data-misc/blob/main/ocean_fixed_stations.csv.

    Using default values all PIRATA buoys are selected.

    Parameters
    ----------
    lonmin: integer or float
        Minimum value of longitude for the weather buoy search area. lonmin need to be in [-180; 180] range. The default lonmin value is -66.0.
    lonmax: integer or float
        Maximum value of longitude for the weather buoy search area. lonmax need to be in [-180; 180] range. The default lonmin value is 8.0.
    latmin: integer or float
        Minimum value of latitude for the weather buoy search area. The default latmin value is -63.0.
    latmax: integer or float
        Maximum value of latitude for the weather buoy search area. The default latmax value is 21.0.
    responsible: string
        Institution responsible by buoy maintenance. This value must be in agreement with one of the values of the responsible column of database (https://github.com/douglasnehme/data-misc/blob/main/ocean_fixed_stations.csv).

    Returns
    -------
    database: pandas.DataFrame
        Database rows of buoys that was inside desired area and are maintained by chosen institution
    '''
    
    database_path = (
        'https://raw.githubusercontent' +
        '.com/douglasnehme/data-misc/' +
        'main/ocean_fixed_stations.csv'
    )
    database = pd.read_csv(
        database_path,
        sep=',',
        header=0,
        na_values=-9999.00
    )
    database = database[
        database.responsible == responsible
    ]
    database = database[
        (database.lon >= lonmin) &
        (database.lon <= lonmax) &
        (database.lat >= latmin) &
        (database.lat <= latmax)
    ]

    return database

def get_weather_data(
    database,
    user,
    password,
    localpath):
    '''
    Get PIRATA weather buoys data.

    Parameters
    ----------
    database: pandas.DataFrame
        The return of the function spatial_filter or a pandas.DataFrame with my weather buoys' database pattern (access https://github.com/douglasnehme/data-misc/blob/main/ocean_fixed_stations.csv).
    user: string
        User to access PMEL ftp server
    password: string
        Password to access PMEL ftp server
    
    Returns
    -------
    buoys_weather_data: dict
        A dict with the buoys name (str) as keys and buoys data (pandas.DataFrame) as values.
    '''

    server = 'ftp.pmel.noaa.gov'
    ftp_path = './high_resolution/ascii/hr'
    local_path = localpath
    buoys_filelist = dict()

    with ftp.FTPHost(
        server,
        user,
        password) as host:
        files = host.listdir(ftp_path)
        for buoy in database.short_name:
            buoys_filelist[buoy] = list()
            for file in files:
                if buoy in file:
                    print(file)
                    host.download(
                        ftp_path + '/' + file,
                        local_path + '/' + file
                    )
                    buoys_filelist[buoy].append(file)

    for buoy, files in buoys_filelist.items():
        for compressed in files:
            uncompressed = subprocess.Popen([
                'tar',
                '-xzf',
                compressed
            ])

    
    stop



    buoys_weather_data = dict()

    # Already identified suffixes in PNBOIA
    # data paths. New elements can be add
    # to the list, but old elements should
    # not be deleted
    suffixes = ['', '1', '_0', '_1']

    for _, row in database.iterrows():
        # Get the string with data paths
        # with leading and trailing square
        # brackets removed
        paths = row.historical_data_path[1:-1]

        weather_path = paths.split(', ')[0]
        # adcp_path = paths.split(', ')[1]

        # Check if weather_path is an empty
        # string (best way to do this
        # according PEP8)
        if not weather_path:
            paths = row.operational_data_path[1:-1]

            weather_path = paths.split(', ')[0]

        for suffix in suffixes:
            wpath_suffix = (
                weather_path[:-4] +
                suffix +
                weather_path[-4:]
            )
            try:
                data = pd.read_csv(
                    wpath_suffix,
                    sep=',',
                    header=0,
                    na_values=[-9999, -9999.0],
                    parse_dates=True,
                    index_col=[0],
                    infer_datetime_format=True
                )

                buoys_weather_data[row.short_name] = data

                break

            except HTTPError as err:
                if err.code == 404:
                    pass
                else:
                    raise

    return buoys_weather_data

def time_filter(
    buoys_weather_data,
    timemin,
    timemax
    ):
    '''
    Filter weather buoys data by time.

    Parameters
    ----------
    buoys_weather_data: dict
        The return of the function get_weather_data or a dict with buoys name as keys and buoys data as pandas.DataFrame with pd.DatetimeIndex as values
    timemin: datetime
        First time step of desired weather buoys data
    timemax: datetime
        Last time step of desired weather buoys data
    
    Returns
    -------
    weather_data_time_filtered = dict        
        A dict with the same pattern of buoys_weather_data, but with just the buoys that had data in desired time period
    '''

    weather_data_time_filtered = dict()

    for buoy in buoys_weather_data.keys():
        filtered = buoys_weather_data[buoy][
            (buoys_weather_data[buoy].index >= timemin) &
            (buoys_weather_data[buoy].index <= timemax)]
        
        if not filtered.empty:
            weather_data_time_filtered[buoy] = filtered

    return weather_data_time_filtered

obsdir = '/home/douglas/Dropbox/profissional/ponto-project/data/buoy'
# obsdir = os.environ[
#     'DATATYPE_DIR'
# ]
user = os.environ[
      'PMEL_USER'
]
password = os.environ[
      'PMEL_PASSWORD'
]
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
buoys_spatial_filtered = spatial_filter(
    lonmin,
    lonmax,
    latmin,
    latmax
)
buoys_weather_data = get_weather_data(
    buoys_spatial_filtered,
    user,
    password,
    obsdir
)
weather_data_time_filtered = time_filter(
    buoys_weather_data,
    timemin,
    timemax
)
############################################
# IMPORT AND MANIPULATE DATA ###############
############################################
# Test if the weather_data_time_filtered 
# dict is empty or not
if weather_data_time_filtered:
    for buoy, df in weather_data_time_filtered.items():
        
        # Station
        print((
            '>>>> Getting PIRATA weather' +
            ' data from {0}').format(
                buoy))

        # Rename index column
        df.index.name = 'datetime'
        
        # Save processed file
        df.to_csv(
            os.path.join(
                obsdir,
                ('weather_pirata_{0}' +
                '.csv').format(
                    buoy)),
            na_rep='NaN')
else:
    print(('>>>> Not available PIRATA' +
    ' weather data for desired area ' +
    'and time'))
