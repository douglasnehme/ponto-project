# Get full path of the present script
fullpath="$(dirname "${BASH_SOURCE[0]}")"

# Set global variables
set -a
. "$fullpath/../ponto.input"
set +a


if [ "$AUTO_DATADIR" = "no" ]; then
    export DATADIR=$YOUR_DATADIR

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
