#!/bin/bash

export HOME=/home/pi
export LOGNAME=pi
export USER=pi
export TERM=linux
export SHELL=/bin/bash

export VENV=/home/pi/sensors_balloon/sensors

export PATH=$VENV/bin:/usr/local/bin:/usr/bin:/bin
unset PYTHONHOME

cd $VENV
python3 $HOME/sensors_balloon/src/sensors.py

