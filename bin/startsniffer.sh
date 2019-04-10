#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Please check again. Usage: startsniffer <Network Interface> <Interval in minutes>"
    exit 1
fi

interface=$1
interval=$2

#username variable
name=$(logname)

#color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

#starting the crawler in a seperate window
konsole --noclose -e /usr/bin/python3 /home/$name/Desktop/NetworkEngineering2/sniff.py $interface $interval &


echo ""
#echo "Starting the web application... This might take some seconds."

#opening up the web application in firefox
#sudo -H -u $name bash -c "sleep 5 && /usr/bin/firefox --new-window https://127.0.0.1:5000/"

#echo -e "${GREEN}Web application started.${NC}"
