#!/bin/bash

#user variable
name=$(logname)

echo "Starting the web application... This might take some seconds."

#opens the web application
/usr/bin/python3.6 /home/$(logname)/Desktop/NetworkEngineering2/app.py &
sudo -H -u $name bash -c "sleep 5 && /usr/bin/firefox --new-window http://127.0.0.1:5000/"
