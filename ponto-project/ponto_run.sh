#!/bin/bash
# OBJECTIVE: Start the Ponto Project system 

#################################################
#### Input File Definiiton ######################
#################################################
# If you set INPUT as "default" the Ponto
# Project system will use the configurations set
# in the ponto.input file located in the same
# folder of this ponto_run.sh script. But you can
# set INPUT as an specific folder where your
# ponto.input file is located. If the ponto.input
# file does not exist in the rigth path the
# system will not work. 
INPUT="default"

#################################################
#### DO NOT CHANGE FROM HERE ####################
#################################################
# Get full path of the present script
fullpath="$(dirname "${BASH_SOURCE[0]}")"

# Set system configuration file
if [ "$INPUT" = "default" ]; then
    INP_FILE="$fullpath/ponto.input"
else
    INP_FILE="$INPUT"
fi

# Set global variables
set -a
. "$INP_FILE"
set +a

if [ "$AUTO_DATADIR" = "no" ]; then
    export DATADIR=$YOUR_DATADIR
    export LOGFILE="$DATADIR/log"

    if [ ! -d "$DATADIR" ]; then
        mkdir "$DATADIR"
        "$fullpath/ponto_main.sh"
    else
        "$fullpath/ponto_main.sh"
    fi
    
elif [ "$AUTO_DATADIR" = "yes" ]; then
    "$fullpath/ponto_main.sh"

else
    touch "$ROOTDIR/log.error"
    echo -e "\nFollow the instructions to the" \
    "correct definition of AUTO_DATADIR in" \
    "$ROOTDIR/ponto.input file\n" |& tee -a \
    "$ROOTDIR/log.error"

fi
