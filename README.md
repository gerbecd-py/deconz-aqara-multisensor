# deconz-aqara-multisensor
Python script, to poll data from deCONZ REST API - returns sensor data for Temperature, Pressure and Humidity. This data is then written to a INFLUX Database, so that it can be visualised in Grafana.

Tested on AQARA Multisensor, Model: WSDCGQ11LM

## Prerequisites
- Running deCONZ / Phoscon APP with sensors added
- Running INFLUX Database

On how to ensure this, please refer to respective documentation.

## Required Python3 Modules
The following Python3 Modules need to be installed (either locally or system wide):
- json
- urllib.request
- datetime
- pytz
- influxdb
- argparse

You can you the command:
###
    python3 -m pip install <module>

## deCONZ API Key

Documentation on how to obtain the deCONZ API Key can be found here:
https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/

## Some configuration is required to run successfully

To run this script, some configuration in the script will be needed. Please change the following, found in the script "*General Configuration*" and "*InfluxDB Configuration*":

- General Configuration
    - deconzServerIPandPort = "CHANGE" -> deCONZ / Phoscon App Server IP and Port (if port is not 80)
    - deconzAPIKey = "CHANGE" -> deCONZ / Phoscon App API Key

- InfluxDB Configuration
    - databaseHost = "CHANGE" -> Hostname where your InfluxDB is running
    - databasePort = "CHANGE" -> Port for communication, Typically 8086
    - databaseDatabase = "CHANGE" -> Database name to write to
    - databaseUsername = "CHANGE" -> Username for the Database
    - databasePassword = "CHANGE" -> Password for the User

## Automate polling

If you wish to automate the polling, you could use crontab. Example crontab entry:

###
    * * * * * /usr/bin/python3 /home/user/python/test/deconz_aqara_multisensor.py

This entry will run the script each minute and write the data to InfluxDB

## Future:
- ver: 0.4
    - Implement error handling

## Changelog:
- ver: 0.3
    - added user authentication for the InfluxDB
- ver: 0.2
    - importing only the modules that are needed - speed up the processing
    - changed var "client" to "influxClient" for easier reading
    - time needs to consider daylight savings time while writing to InfluxDB
    - convert data collection, return to functions
    - get list of sensors to use from API, without Manual setting (var: EnvSensorNames).
- ver: 0.1
    - initial version
