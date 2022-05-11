#!/bin/bash
# OBJECTIVE: Orchestrate the automated
#            download of different types of
#            oceanographic data based on
#            spatial and temporal limits
#            set on a configuration file

# Create log start message
start_msg="### STARTED AT `date` ##\n"

# Workaround to make shell understand conda
# commands
source $CONDA_SH_PATH
conda activate $CONDA_ENV

# Transform $DATATYPE from a string with |
# signs into an array. IFS need to be the
# sign that separate array items on 
# $DATATYPE string
IFS='|'
DATATYPE=($DATATYPE)

############################################
# Structure folders tree ###################
############################################
# Check if DATADIR directory exists, if not
# create it and a log file
if [ -d "$DATADIR" ]; then
    FS_check_datadir_msg=">> Data folder exists in $DATADIR"
else
    mkdir "$DATADIR"
    touch "$LOGFILE"
    FS_check_datadir_msg=">> Creating data folder in $DATADIR"
fi

# Register start message in log
echo -e $start_msg >> "$LOGFILE"

# Register FE check in log
echo "Step: Folder Structure" |& tee -a \
"$LOGFILE"
echo "----------------------" |& tee -a \
"$LOGFILE"
echo -e "$FS_check_datadir_msg\n" |& tee \
-a "$LOGFILE"

# Check if exist folders with each DATATYPE
# name, if not create then

# Iterate over each string of DATATYPE array
for name in ${DATATYPE[*]}; do
    DATATYPE_DIR="$DATADIR/$name"
    if [ -d "$DATATYPE_DIR" ]; then
        FS_check_datatype_dir_msg=">> Folder $DATATYPE_DIR exists"        
    else
        mkdir "$DATATYPE_DIR"
        FS_check_datatype_dir_msg=">> Creating $DATATYPE_DIR"
    fi
    echo $FS_check_datatype_dir_msg |& tee -a \
    "$LOGFILE"
done
############################################
# Download and process data ################
############################################

echo -e "\n\nStep: Data Download" |& tee \
-a "$LOGFILE"
echo "-------------------" |& tee -a \
"$LOGFILE"

# Check if any data has been downloaded into
# each above folders
for name in ${DATATYPE[*]}; do
    # Add DATATYPE_DIR as a shell environment
    # variable, which is read by python
    # scripts as the path to save data
    export DATATYPE_DIR="$DATADIR/$name"
    
    # Check if DATATYPE_DIR is empty
    # The "| read" command prevent find
    # function print the path evaluated on
    # screen
    if find "$DATATYPE_DIR" -maxdepth 0 \
    -empty | read; then
        
        # Loop to run all download script
        # on each subfolder of SCRIPTDIR
        for script in "$SCRIPTDIR/$name/"download*; do
            
            echo -e ">> Searching for" \
            "$name data" |& tee -a \
            "$LOGFILE"
            echo -e ">> Please wait, it can take" \
            "some minutes" |& tee -a \
            "$LOGFILE"
            
            # Get script extension suffix to
            # properly run it
            ext="${script:(-2)}"
            
            if [ "$ext" = "py" ]; then
                $PATH_PYTHON $script |& \
                tee -a "$LOGFILE"
                echo -e "\n" |& tee -a \
                "$LOGFILE"
                
            elif [ "$ext" = "sh" ]; then
                $script |& tee -a "$LOGFILE"
                echo -e "\n" |& tee -a \
                "$LOGFILE"
            fi
        done
        
        # Condition to test if process
        # scripts exist in each SCRIPTDIR
        # subfolder
        # The "2>/dev/null" command prevent
        # find function print an error
        # message when do not exist a
        # process script in that path
        if find "$SCRIPTDIR/$name/"process*.py \
        2>/dev/null | read; then
            # Loop to run each process
            # script individually if more
            # than one exist
            for script in "$SCRIPTDIR/$name/"process*; do
                echo -e "\n>> Processing" \
                "..." |& tee -a "$LOGFILE"

                $PATH_PYTHON $script |& \
                tee -a "$LOGFILE"
                
                echo -e "\n" |& tee -a \
                "$LOGFILE"
            done
        fi
    else
        echo "Folder $DATATYPE_DIR is" \
        "not empty" |& tee -a "$LOGFILE"
    fi
done

conda deactivate

echo -e "\n### ENDED AT `date` ##\n\n\n" \
>> "$LOGFILE"
