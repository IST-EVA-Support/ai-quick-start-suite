#!//bin/bash

LB='\033[1;33m'
NC='\033[0m' # No Color

# echo message with color
message_out(){
    echo -e "${LB}=> $1${NC}"
}

get_script_dir () {
    SOURCE="${BASH_SOURCE[0]}"
    # While $SOURCE is a symlink, resolve it
    while [ -h "$SOURCE" ]; do
        DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
        SOURCE="$( readlink "$SOURCE" )"
        # If $SOURCE was a relative symlink (so no "/" as prefix, need to resolve it relative to the symlink base directory
        [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
    done
    DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
    echo "$DIR"
}

# if the python plugin is already exist in eva plugins python folder, remove it
message_out "check eva plugings folder..."
if [ -f "/opt/adlink/eva/plugins/python/geocheck.py" ]
then
    message_out "/opt/adlink/eva/plugins/python/geocheck.py exist, will remove it first."
    sudo rm /opt/adlink/eva/plugins/python/geocheck.py
    message_out "geocheck.py is removed."
else
    message_out "/opt/adlink/eva/plugins/python/geocheck.py does not exist, will copy it"
fi

# # install requirement dependency
# message_out "install python require package for this plugin......"
# pip3 install shapely

# copy python plugin to eva plugins python folder
message_out "start copying to /opt/adlink/eva/plugins/python ......"
sudo cp ./geocheck.py /opt/adlink/eva/plugins/python/.
message_out "copy done"

# clear cache of gstreamer
message_out "clear cache of gstreamer..."
if [ -f "~/.cache/gstreamer-1.0/registry*" ]
then
    message out "registry exists, will clean it."
    rm ~/.cache/gstreamer-1.0/registry*
else
    message_out "registry is clean."
fi

message_out "Build plugin, geocheck, process completed!"
