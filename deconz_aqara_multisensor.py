from json import loads
import urllib.request
from datetime import datetime
from pytz import timezone
from influxdb import InfluxDBClient

"""
Query deCONZ Zigbee Gateway specificly for AQARA Multi Sensor, which provides
temperature, humidity and pressure data.

Query via deCONZ REST API

Target Users: Myself
Target System: GNU/Linux
Interface: Command Line
Functional Requirements: return sensor data for data set: Temperature, Pressure, Humidity and write data to influxdb
Testing: Simple run test - expecting result in influxdb.
Python Requirements: influxdb (python3 -m pip install influxdb)
API KEY for deCONZ: CABDBA56C4

Written by: david (dot) gerbec (at) me (dot) com

Req:
- ver: 0.3
    [ ] Implement error handling

Changelog:
- ver: 0.2
    [*] importing only the moudules that are needed - speed up the processing
    [*] changed var "client" to "influxClient" for easier reading
    [*] time needs to consider daylight savings time while writing to influxdb
    [*] convert data collection, return to functions
    [*] get list of sensors to use from API, without Manual setting (var: EnvSensorNames).

- ver: 0.1
    * initial version
"""

___version___ = 0.3

# Global Variables
url = "http://10.0.5.251:8090/api/CABDBA56C4/sensors/"
aqaraSesnorIdentifier = "LUMI"
aqaraSensorModelID = "lumi.weather"
aqaraSensorTypeTemperature = "ZHATemperature"
aqaraSensorTypeHumidty = "ZHAHumidity"
aqaraSensorTypePressure = "ZHAPressure"


# InfluxDB Configuration
databaseHost = "10.0.5.250"
databasePort = "8086"
databaseDatabase = "testInstance"

def getAPIResult():

    """
    Function to get the REST API result needed from "url"
    """

    # Get data from REST API
    restApiUrlOpen = urllib.request.urlopen(url, timeout=5).read()
    result = loads(restApiUrlOpen)
    return result

def getEnvSensors():

    """
    Function to get a List - EnvSensorNames with all enviroment sensors names from the AQARA Sensor
    """

    contents = getAPIResult()

    EnvSensorNames = []
    for key, value in contents.items():

        # Convert Key values (based on REST API return of "url")
        contentsSensorIdentifier = contents[key]['manufacturername']
        contentsSensorModelID = contents[key]['modelid']
        contentsSensorName = contents[key]['name']
        contentsSensorType = contents[key]['type']

        if contentsSensorIdentifier == aqaraSesnorIdentifier and contentsSensorModelID == aqaraSensorModelID:

            if contentsSensorType == aqaraSensorTypeTemperature or contentsSensorType == aqaraSensorTypeHumidty or contentsSensorType == aqaraSensorTypePressure:

                # Append Sensor name to List
                EnvSensorNames.append(contentsSensorName)

    # Convert to uniqe entries only
    EnvSensorNames = list(set(EnvSensorNames))

    return EnvSensorNames

def connectToDatabase():

    """
    Function to initiate Database Connection
    """

    # Database Connection: (influxdb)
    influxClient = InfluxDBClient(host=databaseHost, port=databasePort, database=databaseDatabase)

    return influxClient

def getEnvSensorValues():

    """
    Thin function poll data from REST API creates DICT with correct format for INFLUXDB and inserts the data to the InfluxDB.
    """
    sensorDataJsonBody = {}
    sensorDataJsonBody['time'] = datetime.now(timezone('Europe/Vienna'))

    data = getAPIResult()

    for key, value in data.items():

        dataSensor = data[key]['name']
        dataSensorType = data[key]['type']

        sensorName = getEnvSensors()
        for i in range(len(getEnvSensors())):

            if dataSensor == sensorName[i] and dataSensorType == aqaraSensorTypeTemperature:

                sensorDataJsonBody['measurement'] = sensorName[i]
                sensorDataJsonBody['tags'] = { 'sensor': 'temperature' }
                sensorDataJsonBody['fields'] = { 'value': data[key]['state']['temperature'] }
                connectToDatabase().write_points([sensorDataJsonBody])

            elif dataSensor == sensorName[i] and dataSensorType == aqaraSensorTypeHumidty:

                sensorDataJsonBody['measurement'] = sensorName[i]
                sensorDataJsonBody['tags'] = { 'sensor': 'humidity' }
                sensorDataJsonBody['fields'] = { 'value': data[key]['state']['humidity'] }
                connectToDatabase().write_points([sensorDataJsonBody])

            elif dataSensor == sensorName[i] and dataSensorType == aqaraSensorTypePressure:

                sensorDataJsonBody['measurement'] = sensorName[i]
                sensorDataJsonBody['tags'] = { 'sensor': 'pressure' }
                sensorDataJsonBody['fields'] = { 'value': data[key]['state']['pressure'] }
                connectToDatabase().write_points([sensorDataJsonBody])

    return

getEnvSensorValues()
