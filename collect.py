#!/usr/bin/env python3

import requests
import pprint
import time

# config
endpoint = 'http://www.pm25.in/api/querys/aqi_details.json'
payload = {
    'token': '5j1znBVAsnSf5xQyNQyq',
    'city': 'hangzhou',
    'avg': 'false',
}
headers = {
    'user-agent': 'PyAirQualityCollector/0.1 (+https://github.com/Jamesits/PyAirQualityCollector)'
}
measurement_name = 'air_quality'
station_tags = frozenset((
    'area',
    'position_name',
    'station_code',
))
station_fields = frozenset((
    'aqi',
    'co',
    'no2',
    'o3',
    'pm10',
    'pm2_5',
    'primary_pollutant',
    'quality',
    'so2',
))
station_time = 'time_point'

# program
r = requests.get(endpoint, params=payload, headers=headers)
# pprint.PrettyPrinter().pprint(r.json())
for point in r.json():
    # get time
    timestamp = int(time.mktime(time.strptime(point[station_time], '%Y-%m-%dT%H:%M:%SZ'))  * 1000000000)
    # construct tags
    tags = ','.join(['='.join([key, str(value)]) for key, value in {key:point[key] for key in station_tags}.items()])
    # construct datapoints
    data = ','.join(['='.join([key, str(value)]) for key, value in {key:point[key] for key in station_fields}.items()])
    # print as InfluxDB line protocol
    # https://docs.influxdata.com/influxdb/v1.1/write_protocols/line_protocol_reference/
    infline = "{},{} {} {}".format(measurement_name, tags, data, timestamp)
    print(infline)
