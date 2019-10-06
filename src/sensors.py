#!/usr/bin/env python3

import time
import board
import busio
from adafruit_as726x import Adafruit_AS726x
import adafruit_fxas21002c
import adafruit_fxos8700
import adafruit_sht31d
from python_tsl2591 import tsl2591
import datetime
import csv
import os
from itertools import chain

"""
types of sensors 
Light 
Gyroscope
Accelerometer 
"""

def intilize_sensors():

    try:
        light = Adafruit_AS726x(i2c)
        sensors.append('light')
    except:
        pass

    try:
        accelerometer = init_accelerometer(i2c)
        sensors.append('accelerometer')
    except:
        pass

    try:
        gyroscope = init_gyro(busio.I2C(board.SCL, board.SDA))
        sensors.append('gyroscope')
    except:
        pass

    try:
        TempHum = adafruit_sht31d.SHT31D(i2c)
        sensors.append('TempHum')
    except:
        pass

    return light, accelerometer, gyroscope, TempHum, sensors

#todo add try loops around each to ensure that it one does not initilise all the others are still avaiable

def read_light(sensor):

    sensor.conversion_mode = sensor.MODE_2

    v = sensor.violet
    b = sensor.blue
    g = sensor.green
    y = sensor.yellow
    o = sensor.orange
    r = sensor.red

    return v,b,g,y,o,r


def init_gyro(i2c,dps=250):
    # default is 250 DPS, but you can use 500, 1000, or 2000 DPS values):
    if  dps == 250:
        gyroscope = adafruit_fxas21002c.FXAS21002C(i2c)

    elif dps == 500:
        gyroscope = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_500DPS)

    elif dps == 1000:
        gyroscope = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_1000DPS)

    elif dps == 2000:
        gyroscope = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_2000DPS)

    return gyroscope


def read_gyroscope(sensor):

    #read the gyroscope values every second as a default and print them out.
    # Read gyro.
    gyro_x, gyro_y, gyro_z = sensor.gyroscope
    # Print values.
    print('Gyroscope (radians/s): ({0:0.3f},  {1:0.3f},  {2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
    # Delay for a second.

    gyro_x = round(gyro_x,4)
    gyro_y = round(gyro_y,4)
    gyro_z = round(gyro_z,4)


    return gyro_x, gyro_y, gyro_z


def init_accelerometer(i2c, range=2):
    # default is 2G, but you can use 4G or 8G values):

    if range == 2:
        sensor = adafruit_fxos8700.FXOS8700(i2c)

    elif range == 4:
        gyroscope = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_4G)

    elif range == 8:
        gyroscope = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_8G)

    return sensor


def read_accelerometer(sensor):

    # Read acceleration & magnetometer.
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    # Print values.
    print('Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(accel_x, accel_y, accel_z))
    print('Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(mag_x, mag_y, mag_z))

    accel_x = round(accel_x,2)
    accel_y = round(accel_y,2)
    accel_z = round(accel_z,2)
    mag_x   = round(accel_x,3)
    mag_y   = round(accel_y,3)
    mag_z   = round(accel_z,3)

    return accel_x, accel_y, accel_z, mag_x, mag_y, mag_z


def read_temphum(sensor):
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    temp = sensor.temperature
    hum = sensor.relative_humidity

    temp = round(temp,1)
    hum  = round(hum,1)

    # every 10 passes turn on the heater for 1 second

#todo test the efffect of the heater being on or off

    # sensor.heater = True
    # #print("Sensor Heater status =", sensor.heater)
    # time.sleep(1)
    # sensor.heater = False
    # #print("Sensor Heater status =", sensor.heater)
    return temp, hum


def read_tsl(sensor, gain=1, intergration_t=1):
    sensor.set_gain(gain)
    sensor.set_timing(intergration_t)
    full, ir = sensor.get_full_luminosity()  # Read raw values (full spectrum and infared spectrum).
    lux = sensor.calculate_lux(full, ir)  # Convert raw values to Lux.

    print(lux,full, ir)

    return lux, full , ir

def write_file(data, fname ,headings, path='./'):
    now = datetime.datetime.now()
    today = now.strftime("%Y%m%d")

    # TODO make method for constructing the full path with file type exention
    full_name = fname+'.csv'
    full_path = path+full_name
    print("full_path ", full_path)

    try:
        if os.path.isfile(full_path):
            with open(full_path, 'a', newline='') as f:
                wr = csv.writer(f, quoting=csv.QUOTE_NONE)
                wr.writerow(data)
            return
       
        open(full_path, 'a').close()

        with open(full_path, 'w', newline='') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            #wr =csv.writer(f, quoting=csv.QUOTE_NONE)
            wr.writerow(headings)
            return

    except Exception as e:
        print('Trying to write the log.csv file')
        print(e)
        pass

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    #sensors =['light', 'accelerometer','gyroscope','TempHum']

    sensors = []
    headings = []
    data_values = []
    delay = 10
    #data_path = '/home/pi/sensors_balloon/'
    data_path = '/home/pi/'

    first_pass = True
    
    try:
        light = Adafruit_AS726x(i2c)
        sensors.append('light')
    except:
        pass
    
    try:
         accelerometer = init_accelerometer(i2c)
         sensors.append('accelerometer')
    except:
         pass
    
    try:
        gyroscope = init_gyro(busio.I2C(board.SCL, board.SDA))
        sensors.append('gyroscope')
    except:
        pass
    
    try:
        temphum = adafruit_sht31d.SHT31D(i2c)
        sensors.append('temphum')
    except:
        pass

    try:
        tsl = tsl2591()  # initialize
        sensors.append('tsl')
    except:
        pass


    print(sensors)

    while True:

        if 'accelerometer' in sensors:
             data_values.append(read_accelerometer(accelerometer))
             if first_pass == True:
                 headings.append(('accel_x', 'accel_y', 'accel_z', 'mag_x', 'mag_y', 'mag_z'))

        if 'gyroscope' in sensors:
             data_values.append(read_gyroscope(gyroscope))
             if first_pass == True: 
                 headings.append(('gyro_x', 'gyro_y', 'gyro_z'))

        if 'light' in sensors:
             data_values.append(read_light(light))
             if first_pass == True:
                 headings.append(('v','b','g','y','o','r'))

        if 'temphum' in sensors:
             data_values.append(read_temphum(temphum))
             if first_pass == True:
                 headings.append(('t','h'))

        if 'tsl' in sensors:
             data_values.append(read_tsl(tsl))
             if first_pass == True:
                 headings.append(('lux','full','ir'))


#        print('data_values = ',data_values)
        data_list = list(chain.from_iterable(data_values))    #list of lists to a simple list
 #       print('data_list = ',data_list)
#        print('headings = ',headings)
        headings_list = list(chain.from_iterable(headings))   #list of list to a simple list
        print('headings_list = ',headings_list)

        data_list.append(datetime.datetime.now().timestamp())
        headings_list.append('time')
        data_list_float = [float(x) for x in data_list]       # convert any strings to floats 
        #print(headings_list)
        #print(data_list)
        print(data_list_float)

        #todo  clean up the data by converting the tuples to list and croping the floats
        write_file(data_list_float,"data",headings_list,data_path)
        #todo add a second write; a telemetry csv, need to pop the values not wanted for transmission
        data_values = []  # remove the values now stored in the csv files
        time.sleep(delay)
        first_pass = False
        print('-------------\n')
        print('\n')

    #todo write the values to a csv file in a partucular directory
