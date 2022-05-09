#!/bin/bash
# AUTOR: Douglas Medeiros Nehme
# PLACE: Rio de Janeiro - Brazil
# CONTACT: medeiros.douglas3@gmail.com
# CRIATION: mar/2021
# OBJECTIVE: Download global EN4 profiles
#            with Gouretski and Reseghetti
#            (2010) corrections for 2019 and
#            2020

obsdir=/home/douglasnehme/

fname2019=EN.4.2.1.profiles.g10.2019.zip
fname2020=EN.4.2.1.profiles.g10.2020.zip

cd $obsdir

# Download data
wget --verbose --show-progress --https-only \
https://www.metoffice.gov.uk/hadobs/en4/\
data/en4-2-1/$fname2019
wget --verbose --show-progress --https-only \
https://www.metoffice.gov.uk/hadobs/en4/\
data/en4-2-1/$fname2020

# Extract nc files and remove zip ones
unzip $fname2019
rm -r $fname2019

unzip $fname2020
rm -r $fname2020

# Remove 2019 files that will not be used
rm -r EN.4.2.1.f.profiles.g10.20190*.nc
rm -r EN.4.2.1.f.profiles.g10.201910.nc
rm -r EN.4.2.1.f.profiles.g10.201911.nc
