Installation
------------

on a fresh install of Raspbian Buster lite

### upgrade the system

sudo apt-get update

sudo apt-get upgrade

install pip and venv  (may be needed on Lite versions of Raspbian)

sudo apt-get install python3-pip

sudo pip3 install --upgrade setuptools

sudo apt-get install python3-venv


## Fetch the repo

git clone git@github.com:albioninnovate/sensors_balloon.git

## create and activate the virtual environment
cd sensors_balloon

make

if the virtual environment does not start:

source ./bin/activate


## install the requirements

pip3 install -e ./

if that does not work try :

pip3 install -r requirements-freeze.txt

pip3 install -e ./


# Or manually:

Create and activate Virtual Environment
---------------------------------------

sudo apt-get install python3-venv

python3 -m venv ./sensors
source ./sensors/bin/activate

Install pip and setuptools
--------------------------
(not automaticly installed on lite versions of raspbian)

sudo apt-get install python3-pip

sudo pip3 install --upgrade setuptools


Install and enable I2C
----------------------
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools

### enable i2C interface via

sudo raspi-config


### Install Circuit Python

ref: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

### Install Python libraries
pip3 install RPI.GPIO
pip3 install adafruit-blinka

#### for the specific sensors
sudo pip3 install adafruit-circuitpython-sht31d 
sudo pip3 install adafruit-circuitpython-as726x
sudo pip3 install adafruit-circuitpython-fxos8700
sudo pip3 install adafruit-circuitpython-fxas21002c


(#TODO test with and with out  pip3 install adafruit-circuitpython-lis3dh)

to test run:   sudo sht31d_test.py
(#TODO  Investigate need  for sudo) 



NXP Precision 9DoF Breakout
---------------------------


Ref: 
https://learn.adafruit.com/nxp-precision-9dof-breakout/python-circuitpython

https://circuitpython.readthedocs.io/projects/fxos8700/en/latest/

sudo pip3 install adafruit-circuitpython-fxos8700
sudo pip3 install adafruit-circuitpython-fxas21002c


### Power Pins

	VIN - 3.3-5V input, which feeds the on board 3.3V voltage regulator and optionally sets the signal levels for the I2C pins (SCL and SDA) if you are using a 5V system. On a 3.3V system (any Adafruit Feather, for example), connect 3.3V to VIN for 3.3V logic throughout the system. On a 5.0V system, connect VIN to 5V, and the signals will be shifted downward to 3.3V before reaching the NXP sensors (which are limited to 3.6V or less for the pins).
	3Vo - This is the output of the 3.3V linear regulator on the NXP Precision 9DoF Breakout. On a 5V system, you can use this as an additional 3.3V supply if you need some extra 3.3V power.
	GND - This should be connected to GND on your development board.


### Digital Pins

	SCL - I2C, Connect this to SCL on your development board. This pin is level-shifted and 3-5V logic safe.
	SDA - I2C, Connect this to SDA on your development board. This pin is level-shifted and 3-5V logic safe.
	RST - Optionally connect this to RST on your development board (depending on the logic level used), or to a GPIO pin if you wish to manually reset the sensors on the breakout. This pin isn't required in most circumstances, but can be useful to recover from error conditions on long running systems where the sensors might have entered an unknown config state. This pin is level-shifted and 3-5V logic safe.
	AI1, AI2 - This two pins allow interrupts from the Accelerometer/Magnetometer (see the datasheet for details). These are not level shifted but since they are outputs only, you can use with 3 or 5V logic systems.
	GI1, G12 - These two pins allow interrupts from the Gyroscope (see the datasheet for details). These are not level shifted but since they are outputs only, you can use with 3 or 5V logic systems.


 fxos8700_test.py 
# Simple demo of the FXOS8700 accelerometer and magnetometer.
# Will print the acceleration and magnetometer values every second.
import time     
import board
import busio     
import adafruit_fxos8700
  
# Initialize I2C bus and device.
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxos8700.FXOS8700(i2c)
# Optionally create the sensor with a different accelerometer range (the
# default is 2G, but you can use 4G or 8G values):
#sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_4G)
#sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_8G)

# Main loop will read the acceleration and magnetometer values every second
# and print them out.
while True:
    # Read acceleration & magnetometer.
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    # Print values.
    print('Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(accel_x, accel_y, accel_z))
    print('Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(mag_x, mag_y, mag_z))
    # Delay for a second.
    time.sleep(1.0)






FXAS21002C_test.py 
# Simple demo of the FXAS21002C gyroscope.
# Will print the gyroscope values every second.
import time

import board
import busio

import adafruit_fxas21002c


# Initialize I2C bus and device.
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_fxas21002c.FXAS21002C(i2c)
# Optionally create the sensor with a different gyroscope range (the
# default is 250 DPS, but you can use 500, 1000, or 2000 DPS values):
#sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_500DPS)
#sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_1000DPS)
#sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_2000DPS)

# Main loop will read the gyroscope values every second and print them out.
while True:
    # Read gyroscope.
    gyro_x, gyro_y, gyro_z = sensor.gyroscope
    # Print values.
    print('Gyroscope (radians/s): ({0:0.3f},  {1:0.3f},  {2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
    # Delay for a second.
    time.sleep(1.0)




