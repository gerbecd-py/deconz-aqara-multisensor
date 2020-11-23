# deconz-aqara-multisensor
 Python script, to poll data from deCONZ REST API - returns sensor data for Temperature, Pressure and Humidity. This data is then written to a INFLUX Database,
 so that it can be visualised in Grafana.

 Target System: GNU/Linux
 Interface: Command Line
 Functional Requirements: return sensor data for data set: Temperature, Pressure, Humidity and write data to influxdb
 Testing: Simple run test - expecting result in influxdb.
 Python Requirements: influxdb (python3 -m pip install influxdb)

 Documentation on how to obtain the deCONZ API Key can be found here:
 https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/

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
