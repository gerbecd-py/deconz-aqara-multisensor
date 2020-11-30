# deconz-aqara-multisensor
Python script, to poll data from deCONZ REST API - returns sensor data for Temperature, Pressure and Humidity. This data is then written to a INFLUX Database, so that it can be visualised in Grafana.

## Prerequisites
- Running INFLUX Database

Search documentation for INFLUX setup options on their respective websites.

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

## deCONZ

 Documentation on how to obtain the deCONZ API Key can be found here:
 https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/

## Automate polling

If you wish to automate the polling, you could use crontab. Example crontab entry:

###
    * * * * * /usr/bin/python3 /home/user/python/test/deconz_aqara_multisensor.py

This entry will run the script each minute and write the data to InfluxDB

## Req:
- ver: 0.3
    - Implement error handling

## Changelog:
- ver: 0.2
    - importing only the modules that are needed - speed up the processing
    - changed var "client" to "influxClient" for easier reading
    - time needs to consider daylight savings time while writing to influxdb
    - convert data collection, return to functions
    - get list of sensors to use from API, without Manual setting (var: EnvSensorNames).

- ver: 0.1
    - initial version
