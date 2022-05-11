# :trident: Ponto Project

Automated download of different types of oceanographic data for the South Atlantic Ocean based on spatial and temporal limits.

All data obtained does not and is not intended to undergo any extra treatment beyond that provided by the original sources. However, some minimal modifications are necessary, as in the case of the PIRATA Project data, where all variables of a buoy are gathered in a single file, unlike what is observed in their FTP server.

## More Advanced Stable Version

Version 0.3.1

## Data Bases

- Implemented
  - [PNBOIA (Brazilian National Buoy Program)](https://www.marinha.mil.br/chm/dados-do-goos-brasil/pnboia)
  - [PIRATA Project](https://www.pmel.noaa.gov/gtmba/pmel-theme/atlantic-ocean-pirata)
    - Just the hourly data (one of the sample frequencies named as high resolution by PIRATA Project)
  - [Argo](https://argo.ucsd.edu/) from [EN4](https://www.metoffice.gov.uk/hadobs/en4/)
    - Based on EN4 4.2.2 version

- In Development
  - ...

- Planned
  - [Drifter](https://www.aoml.noaa.gov/phod/gdp/)
  - [SiMCosta (Monitoring System of the Brazilian Coast)](https://simcosta.furg.br/home)
  - Satellite data from different sources
  - Tide Gauges from different sources

## Operating System

As Ponto Project is being developed using Python and Bash it needs to run on UNIX operating systems.

## How to Use the System?

1. Clone the latest version of the [Ponto Project System](https://github.com/douglasnehme/ponto-project)
1. Create a python environment with the minimum required dependencies using [Anaconda platform](https://www.anaconda.com/products/distribution). If you have never used it, you can take your first steps [here](https://docs.anaconda.com/anaconda/user-guide/getting-started/) and [here](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html). If you have some experience you can go to this [point](https://github.com/douglasnehme/ponto-project#conda-environment)
1. Once you have the code and minimum dependency requirements, you need to configure your settings in an input file and define where that file will be saved. Instructions can be read [here](https://github.com/douglasnehme/ponto-project#definition-of-spatial-and-temporal-limits)
1. Run the [ponto_run.sh script](/ponto-project/ponto_run.sh)

### Conda Environment

For a correct use of the Ponto Project system, it is recommended to clone the conda environment used in the development of the current version of the project. If using the terminal you can execute the command below.

`conda create --name <your-env-name> --file ponto-requirements.txt`

### Definition of Spatial and Temporal Limits

The simplest way to configure your settings is to make a copy of the [example.input file](/ponto-project/example.input) naming it ponto.input and save it in the [ponto-project folder](/ponto-project/), the same folder as example.input is located. Then adapt the ponto.input for your purpose with the desired values for:
  
- ROOTDIR: The path where the Ponto Project System was cloned
- CONDA_PATH: The anaconda/miniconda path where you created the python environment
- CONDA_ENV: The name of the python environment
- AUTO_DATADIR and YOUR_DATADIR: Explained at [example.input file](/ponto-project/example.input)
- LON_MIN: Westernmost desired point. Must be in [-180, 180] format
- LON_MAX: Easternmost desired point. Must be in [-180, 180] format
- LAT_MIN: Southernmost desired point
- LAT_MAX: Northernmost desired point
- DATETIME_MIN: Start time limit. Must be in "23-11-2019 21:50:23" format. Based on [strftime documentation](https://strftime.org/) this need to be in the %d-%m-%Y %H:%M:%S format
- DATETIME_MAX: End time limit. Must be in "23-11-2019 21:50:23" format. Based on [strftime documentation](https://strftime.org/) this need to be in the %d-%m-%Y %H:%M:%S format
- DATETYPE: Define what type of data the system will search for. Until now, are implemented the download of weather buoy data from PNBOIA and PIRATA and ARGO float data from EN4. To search for only weather buoy data, DATATYPE must be "buoy". To search for only float data, DATATYPE must be "argo". To search for both data types, DATATYPE must be "buoy|argo". We highlight that the | signal is used as an identifier that more than one data type needs to be searched. Using another separator signal will result in system malfunction.
- PMEL_USER and PMEL_PASSWORD: Username and password to access the FTP server of the Tropical Atmosphere Ocean (TAO) Project of the Pacific Marine Environmental Laboratory (PMEL) and download PIRATA Project data
  - To create your own username and password, please contact one of these emails:
    - [Dai McClurg](mailto:dai.c.mcclurg@noaa.gov)
    - [Kenneth Connell](mailto:kenneth.connell@noaa.gov)
    - [Global Tropical Moored Buoy Array Program](mailto:oar.pmel.taotech@noaa.gov)

If needed, the first lines of the [ponto_run.sh script](/ponto-project/ponto_run.sh) describe the best way to modify the location of the ponto.input that the system understands.
