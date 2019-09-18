import time
import board
import busio
from adafruit_as726x import Adafruit_AS726x
import adafruit_fxas21002c
import adafruit_fxos8700
import adafruit_sht31d


"""
types of sensors 
Light 
Gyroscope
Accelerometer 

"""

# Initialize I2C bus and all sensors.
#i2c = busio.I2C(board.SCL, board.SDA)

def intilize_sensors():
    light = Adafruit_AS726x(i2c)
    accelerometer = init_accelerometer(i2c)
    gyroscope = init_gyro(i2c)
    TempHum = adafruit_sht31d.SHT31D(i2c)

    return light, accelerometer, gyroscope, TempHum

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


def init_gyro(i2c):
    gyroscope = adafruit_fxas21002c.FXAS21002C(i2c)
    # Optionally create the gyroscope with a different gyroscope range (the
    # default is 250 DPS, but you can use 500, 1000, or 2000 DPS values):
    #gyroscope = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_500DPS)
    #gyroscope = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_1000DPS)
    #gyroscope = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_2000DPS)
#todo make these dynamical configrable so the desired ranges and be passed to the function

    return gyroscope


def read_gyroscope(sensor):
    #read the gyroscope values every second as a default and print them out.
    # Read gyro.
    gyro_x, gyro_y, gyro_z = sensor.gyroscope
    # Print values.
    print('Gyroscope (radians/s): ({0:0.3f},  {1:0.3f},  {2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
     # Delay for a second.

    return gyro_x, gyro_y, gyro_z


def init_accelerometer(i2c):
    sensor = adafruit_fxos8700.FXOS8700(i2c)
    # Optionally create the gyroscope with a different accelerometer range (the
    # default is 2G, but you can use 4G or 8G values):
    # gyroscope = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_4G)
    # gyroscope = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_8G)
# todo make these dynamical configrable so the desired ranges and be passed to the function

    return sensor


def read_accelerometer(sensor):
    # Read acceleration & magnetometer.
    accel_x, accel_y, accel_z = sensor.accelerometer
    mag_x, mag_y, mag_z = sensor.magnetometer
    # Print values.
    print('Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(accel_x, accel_y, accel_z))
    print('Magnetometer (uTesla): ({0:0.3f}, {1:0.3f}, {2:0.3f})'.format(mag_x, mag_y, mag_z))

    return accel_x, accel_y, accel_z


def read_TempHum(sensor):
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)

    # every 10 passes turn on the heater for 1 second

    sensor.heater = True
    #print("Sensor Heater status =", sensor.heater)
    time.sleep(1)
    sensor.heater = False
    #print("Sensor Heater status =", sensor.heater)
    temp = sensor.temperature
    hum = sensor.relative_humidity

    return temp, hum

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    print('i2c = ', i2c)

#    light, accelerometer, gyroscope, TempHum = intilize_sensors()
#    print(light, accelerometer, gyroscope, TempHum)

    try:
        light = Adafruit_AS726x(i2c)
    except:
        light_on = 0
        
    accelerometer = init_accelerometer(i2c)
    gyroscope = init_gyro(busio.I2C(board.SCL, board.SDA))
    TempHum = adafruit_sht31d.SHT31D(i2c)


    read_accelerometer(accelerometer)
    read_gyroscope(gyroscope)
#    read_light(light)
    read_TempHum(TempHum)

    #todo write the values to a csv file in a partucular directory
