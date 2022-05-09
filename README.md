# :trident: Ponto Project

Automated download of different types of oceanographic data for the South Atlantic Ocean based on spatial and temporal limits.

All data obtained does not and is not intended to undergo any extra treatment beyond that provided by the original sources. However, some minimal modifications are necessary, as in the case of the PIRATA Project data, where all variables of a buoy are gathered in a single file, unlike what is observed in their FTP server.

## More Advanced Stable Version

Version 0.2.1

## Data Bases

- Implemented
  - [PNBOIA (Brazilian National Buoy Program)](https://www.marinha.mil.br/chm/dados-do-goos-brasil/pnboia)
  - [PIRATA Project](https://www.pmel.noaa.gov/gtmba/pmel-theme/atlantic-ocean-pirata)
    - Just the hourly data (one of the sample frequencies named as high resolution by PIRATA Project)

- In Development
  - [Argo](https://argo.ucsd.edu/) from [EN4](https://www.metoffice.gov.uk/hadobs/en4/)

- Planned
  - [Drifter](https://www.aoml.noaa.gov/phod/gdp/)
  - [SiMCosta (Monitoring System of the Brazilian Coast)](https://simcosta.furg.br/home)
  - Satellite data from different sources
  - Tide Gauges from different sources

## Operating System

As Ponto Project is being developed using Python and Bash it needs to run on UNIX operating systems.

## Conda Environment

For a correct use of the Ponto Project system, it is recommended to clone the conda environment used in the development of the current version of the project by executing the command below in the terminal (the * sign represents the version of the file and needs to be changed).

`conda create --name <your-env-name> --file ponto-v*.txt`

## Definition of Spatial and Temporal Limits

The simplest way is to make a copy of the example.input file and name it ponto.input and save it in the script folder, the same folder as example.input is located. Then adapt the ponto.input for your purpose with the desired values for longitude, latitude, datetime, paths, and your credentials. If needed, the first lines of the ponto_run.sh script describe the best way to modify the location of the ponto.input that the system understands.

To create your own login and password to access PIRATA Project data from the Tropical Atmosphere Ocean (TAO) Project of the Pacific Marine Environmental Laboratory (PMEL) FTP server, please contact one of these emails:

- [Dai McClurg](mailto:dai.c.mcclurg@noaa.gov)
- [Kenneth Connell](mailto:kenneth.connell@noaa.gov)
- [Global Tropical Moored Buoy Array Program](mailto:oar.pmel.taotech@noaa.gov)
