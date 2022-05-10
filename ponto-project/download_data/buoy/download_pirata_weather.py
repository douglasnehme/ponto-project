# -*- coding: utf-8 -*-
# AUTOR: Douglas Medeiros Nehme
# PLACE: Rio de Janeiro - Brazil
# CONTACT: medeiros.douglas3@gmail.com
# CRIATION: apr/2022
# OBJECTIVE: Download PIRATA buoy data for
#            desired area and time

import os
import gzip
import json

import pandas as pd
import ftputil as ftp

from datetime import datetime

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

def is_number(n):
    '''
    
    '''
    is_number = True
    
    try:
        num = float(n)
        # check for "nan" floats
        is_number = num == num
    
    except ValueError:
        is_number = False

    return is_number

def drop_QSID(columns_names):
    '''
    -> Tratamentos que devem ser feitos nas colunas de Quality ['Q', 'QQ', 'QQQ'...] e Source ['S', 'SS', 'SSS'...]:
    
    a) Tranformar as colunas de Quality e Source em inteiros e depois em strings, para que os valores decimais, erroneamente inseridos, sejam eliminados.

    b) Juntar todas as colunas ['Q', 'QQ', 'QQQ'...] e ['S', 'SS', 'SSS'...] que existirem em cada dataframe em colunas únicas chamadas, respectivamente, 'Q' e 'S'.

        b.1) Não sei se isso é a melhor opção, pq se em um bloco tivermos as profundidades de coleta 1, 20, 40 e 120 a coluna de Quality/Source será dada no formato QQQQ. Já se em outro bloco tivermos somente as profundidades 1, 40 e 120 a coluna Quality/Source será dada no formato QQQ e dessa forma as segunda e terceira colunas nos dois blocos representarão profundidades diferentes.

    c) Além disso, se conseguirmos juntar todas as colunas citadas acima em uma para cara parâmetro deveremos incluir um sufixo com o nome do arquivo para diferenciar as colunas entre arquivos, já que terão os mesmos nomes ('Q' e 'S').

    OBS: Após finalizar as questões das colunas acima também trabalhar na de Instrument ['ID', 'IDID', 'IDIDID'...]. Isso porque a questão da coluna Instrument é mais basal que as demais, pois seus valores, em alguns momentos, possuem espaço, o que para o python se confunde com o separador de colunas e demandará mais tempo e deverá ser tratado mais ao início do código.
    '''
    cols2stay, cols2drop = [], []
    q, s, id = 'Q', 'S', 'ID'

    # Create a list of strings with Q, S, and ID
    # repeated so many times, as in PIRATA files
    for i in range(25):
        cols2drop.append(q)
        cols2drop.append(s)
        cols2drop.append(id)

        q += 'Q'
        s += 'S'
        id += 'ID'

    for name in columns_names:
        if name not in cols2drop:
            cols2stay.append(name)

    return cols2stay

def handle_pirata_metadata(filepath):
    '''
    
    '''

    fh = gzip.open(
        filepath,
        'rt'
    ).read()

    linenum = 0
    meta = {
        # tuple with line numbers of file header
        'file_header': (),
        # list of tuples with line numbers of 
        # each data block header
        'block_headers': [()],
        # list of tuples with data sample
        # depth(s) for each data block
        'depth': [()],
        # columns name for each data block
        'cols_name': [()],
        # data unit
        'units': None,
        # NaN value
        'nan': None,
        # lines in the file
        'lines': None,
        # list of extra info
        'extra': [],
    }
    
    # Extract metadata
    for line in fh.split('\n'):
        line = line.lstrip()

        if line.startswith('Location:'):
            meta['file_header'] += (linenum,)

        if line.startswith('Units:'):
            meta['file_header'] += (linenum,)

            for info in line.split(','):
                if 'Units' in info:
                    units = info.split('Units: ')[1]
                    meta['units'] = units.strip()
                    
                    # Condition to manage a problem
                    # in precipitation files headers
                    if 'Precipitation' in info:
                        for nan in line.split(' '):
                            if is_number(nan):
                                meta['nan'] = nan.strip()

                elif 'missing' in info:
                    nan = info.split(' = missing')[0]
                    meta['nan'] = nan.strip()
                else:
                    meta['extra'].append(
                        info.strip()
                    )

        if line.startswith('Time:'):
            meta['block_headers'][-1] += (linenum,)

        if line.startswith('Index:'):
            meta['block_headers'][-1] += (linenum,)

        if line.startswith(('Depth', 'Height')):
            meta['block_headers'][-1] += (linenum,)

            infos = line.split('(M):')[1]

            for info in infos.split(' '):
                # Pass just numbers
                if is_number(info):
                    info = str(int(float(info)))
                    meta['depth'][-1] += (info,)
        
        if line.startswith('YYYYMMDD HHMM'):
            meta['block_headers'][-1] += (linenum,)

            # names = line.split('HHMM')[1]
            names = line.split(' ')

            # Remove all empty values
            while range(names.count('')):
                names.remove('')

            # Add depth as suffix of data
            # columns name
            for i, depth in zip(
                range(len(meta['depth'][-1])),
                meta['depth'][-1]):

                names[i+2] = names[i+2] + '_' + depth

            meta['cols_name'][-1] += tuple(names)

            meta['block_headers'].append(())
            meta['cols_name'].append(())
            meta['depth'].append(())

        linenum += 1

    meta['lines'] = linenum

    # Remove empty tuples
    meta['block_headers'].pop(-1)
    meta['cols_name'].pop(-1)
    meta['depth'].pop(-1)

    return meta

def handle_pirata_data(filepath, meta):
    '''
    
    '''
    # Open each data block separatelly and
    # then concatenate
    data = pd.DataFrame()

    dt_parser = lambda x: datetime.strptime(
        x,
        '%Y%m%d %H%M')

    for i in range(len(meta['block_headers'])):
        current_block = meta['block_headers'][i]
        
        if i+1 < len(meta['block_headers']):
            next_block = meta['block_headers'][i+1]
        else:
            next_block = [meta['lines']]

        skip_rows = range(current_block[-1])
        skip_footer = meta['lines'] - next_block[0]

        current_names = meta['cols_name'][i]
        cols2use = drop_QSID(current_names)
        
        df = pd.read_csv(
            filepath,
            compression='gzip',
            engine='python',
            sep='\s+',
            header=0,
            names=current_names,
            usecols=cols2use,
            skiprows=skip_rows,
            skipfooter=skip_footer,
            na_values=meta['nan'],
            parse_dates={
                'datetime': [
                    'YYYYMMDD',
                    'HHMM'
            ]},
            date_parser=dt_parser,
            index_col='datetime',
        )
        data = pd.concat(
            [data, df],
            join='outer',
            axis='index'
        )

    return data

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
    metadata = dict()
    buoys_weather_data = dict()

    with ftp.FTPHost(
        server,
        user,
        password) as host:

        files = host.listdir(ftp_path)

        for buoy in database.short_name:
            
            buoy_vars = list()
            metadata[buoy] = dict()
            
            for file in files:
                if buoy in file:
                    ftp_filename = os.path.join(
                        ftp_path,
                        file
                    )
                    local_filename = os.path.join(
                        local_path,
                        file
                    )
                    var_name = file.split(buoy)[0]

                    host.download(
                        ftp_filename,
                        local_filename
                    )
                    # Test if the file was
                    # effectively downloaded
                    if os.path.exists(local_filename):

                        meta = handle_pirata_metadata(
                            local_filename
                        )
                        df = handle_pirata_data(
                            local_filename,
                            meta
                        )
                        os.remove(local_filename)

                        # Rename the vars with
                        # the filename preffix
                        # to avoid repeated cols
                        # on final DataFrame
                        for column in df.columns:
                            df.rename(
                                columns={
                                    column: (
                                        column +
                                        '_' +
                                        var_name
                                    )},
                                inplace=True
                            )

                        buoy_vars.append(df)
                        metadata[buoy][var_name] = meta
            
            buoys_weather_data[buoy] = pd.concat(
                buoy_vars,
                axis='columns',
                join='outer'
            )
    
    return buoys_weather_data, metadata

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

obsdir = os.environ[
    'DATATYPE_DIR'
]
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
buoys_weather_data, metadata = get_weather_data(
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
            ' buoy data from {0}').format(
                buoy
        ))
        # Save data file
        df.to_csv(
            os.path.join(
                obsdir,
                ('weather_pirata_{0}' +
                '.csv').format(
                    buoy)),
            na_rep='NaN'
        )
    # Save metadata file
    metapath = os.path.join(
        obsdir,
        'weather_pirata_metadata.json'
    )
    with open(metapath, 'w') as fp:
        json.dump(
            metadata,
            fp,
            indent=4
        )
    
else:
    print((
        '>>>> Not available PIRATA' +
        ' weather buoy data for the' +
        ' desired area and time'
    ))
