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

# Download AI model for Neon-JNX 
wget https://sftp.adlinktech.com/image/onnx/yolov4-416-fp16.engine.zip
mv yolov4-416-fp16.engine.zip NX/yolov4-416-fp16.engine
# Download AI onnx model
wget https://sftp.adlinktech.com/image/onnx/yolov4-416.onnx.zip
mv yolov4-416.onnx.zip misc/yolov4-416.onnx

# geocheck
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

# copy python plugin to eva plugins python folder
message_out "start copying to /opt/adlink/eva/plugins/python ......"
sudo cp ./Plugin/geocheck.py /opt/adlink/eva/plugins/python/.
message_out "copy done"


#GPIO Alert
# if the python plugin is already exist in eva plugins python folder, remove it
message_out "check eva plugings folder..."
if [ -f "/opt/adlink/eva/plugins/python/GPIOAlert.py" ]
then
    message_out "/opt/adlink/eva/plugins/python/GPIOAlert.py exist, will remove it first."
    sudo rm /opt/adlink/eva/plugins/python/GPIOAlert.py
    message_out "GPIOAlert.py is removed."
else
    message_out "/opt/adlink/eva/plugins/python/GPIOAlert.py does not exist, will copy it"
fi

# copy python plugin to eva plugins python folder
message_out "start copying to /opt/adlink/eva/plugins/python ......"
sudo cp ./Plugin/GPIOAlert.py /opt/adlink/eva/plugins/python/.
message_out "copy done"

#email Alert
# if the python plugin is already exist in eva plugins python folder, remove it
message_out "check eva plugings folder..."
if [ -f "/opt/adlink/eva/plugins/python/emailAlert.py" ]
then
    message_out "/opt/adlink/eva/plugins/python/emailAlert.py exist, will remove it first."
    sudo rm /opt/adlink/eva/plugins/python/emailAlert.py
    message_out "emailAlert.py is removed."
else
    message_out "/opt/adlink/eva/plugins/python/emailAlert.py does not exist, will copy it"
fi

# copy python plugin to eva plugins python folder
message_out "start copying to /opt/adlink/eva/plugins/python ......"
sudo cp ./Plugin/emailAlert.py /opt/adlink/eva/plugins/python/.
message_out "copy done"

#SOP Complianace for semiconductor
# if the python plugin is already exist in eva plugins python folder, remove it
message_out "check eva plugings folder..."
if [ -f "/opt/adlink/eva/plugins/python/handup.py" ]
then
    message_out "/opt/adlink/eva/plugins/python/handup.py exist, will remove it first."
    sudo rm /opt/adlink/eva/plugins/python/handup.py
    message_out "handup.py is removed."
else
    message_out "/opt/adlink/eva/plugins/python/handup.py does not exist, will copy it"
fi

# copy python plugin to eva plugins python folder
message_out "start copying to /opt/adlink/eva/plugins/python ......"
sudo cp ./Plugin/handup.py /opt/adlink/eva/plugins/python/.
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

message_out "Build plugin, process completed!"
