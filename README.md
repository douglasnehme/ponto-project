# :trident: Ponto Project
Automated download of different types of oceanographic data for the South Atlantic Ocean based on spatial and temporal limits.

- Implemented
    - [PNBOIA (Brazilian National Buoy Program)](https://www.marinha.mil.br/chm/dados-do-goos-brasil/pnboia)

- In Development
    - [PIRATA](https://www.pmel.noaa.gov/gtmba/pmel-theme/atlantic-ocean-pirata)

- Planned
    - [Argo](https://argo.ucsd.edu/)
    - [Drifter](https://www.aoml.noaa.gov/phod/gdp/)
    - [SiMCosta (Monitoring System of the Brazilian Coast)](https://simcosta.furg.br/home)
    - Satellite data from different sources
    - Tide Gauges from different sources

## Operating System
As Project Ponto is being developed using Python and Bash it needs to run on UNIX operating systems.

## Conda Environment
To clone the conda environment used in the development of the current version of the Ponto Project, use the command below in the terminal (the * sign represents the version of the file and needs to be changed).

`conda create --name <your-env-name> --file ponto-v*.txt`

## Definition of Spatial and Temporal Limits
Set the desired values for longitude, latitude, and datetime in the point.input file.
