import grovepi
import json
import time
import atexit

def returnTemperature():
    # Connect the DHT Sensor to digital port D4
    sensor = 4
    try:
        [temp,humidity] = grovepi.dht(sensor,1)
        return str(temp) + "C"
    except IOError:
        return "Error"

def returnHumidity():
    # Connect the DHT Sensor to digital port D4
    sensor = 4
    try:
        [temp,humidity] = grovepi.dht(sensor,1)
        return str(humidity) + "%"
    except IOError:
        return "Error"

def returnAirquality():
    # Wait 2 minutes for the sensor to heat-up
    # Connect the Grove Air Quality Sensor to analog port A1
    air_sensor = 1
    grovepi.pinMode(air_sensor,"INPUT")
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(air_sensor)
        if sensor_value > 700:
            return "High pollution - reading: " + str(sensor_value)
        elif sensor_value > 300:
            return "Low pollution - reading: " + str(sensor_value)
        else:
            return "Air fresh - reading: " + str(sensor_value)
    except IOError:
        return "Error"

def returnGas():
    # Connect the Grove Gas Sensor to analog port A1
    gas_sensor = 1
    grovepi.pinMode(gas_sensor,"INPUT")
    try:
        sensor_value = grovepi.analogRead(gas_sensor)
        # Calculate gas density - large value means more dense gas
        density = sensor_value * 1.0 / 1024 * 1.0
        return str(density)
    except IOError:
        return "Error"

def returnLight():
    # Connect Light Sensor to analog port A0
    light_sensor = 0
    grovepi.pinMode(light_sensor,"INPUT")
    threshold = 10
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
        # Calculate resistance of sensor in K
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        if resistance > threshold:
            return "dark"
        else:
            return "bright"
    except IOError:
        return "Error"

def returnSound():
    # Connect Sound Sensor to analog port A0
    sound_sensor = 0
    grovepi.pinMode(sound_sensor,"INPUT")
    threshold_value = 400
    try:
        sensor_value = grovepi.analogRead(sound_sensor)
        if sensor_value > threshold_value:
            return "high"
        else:
            return "low"
    except IOError:
        return "Error"

def returnUltrasonic():
    # Connect Ultrasonic Ranger to digital port D4
    ultrasonic_ranger = 4
    try:
        # Read distance value from Ultrasonic
        return str(grovepi.ultrasonicRead(ultrasonic_ranger))
    except TypeError:
        return "Error"
    except IOError:
        return "Error"

dispatcher = {
    u'temperature': returnTemperature,
    u'humidity': returnHumidity,
    u'airquality': returnAirquality,
    u'gas': returnGas,
    u'light': returnLight,
    u'sound': returnSound,
    u'ultrasonic': returnUltrasonic
}
