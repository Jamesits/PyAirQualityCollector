#!/usr/bin/env python3

import requests
import pprint
import time
import sys

# config
api_key = '5j1znBVAsnSf5xQyNQyq'
cities = frozenset((
    'hangzhou',
    'shijiazhuang',
    'qingdao',
    'ningbo',
    'beijing',
    'shanghai',
    'xian',
    'wuhan',
    'shaoxing',
    'taizhou',
    'changchun',
    'zhoushan',
    'shenzhen',
    'suzhou',
    'guangzhou',
    'chengdu',
))
endpoint = 'http://www.pm25.in/api/querys/aqi_details.json'
payload = {
    'token': api_key,
    'city': '',
    'avg': 'true',
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
error_indicator = 'error'

# convert data to specific type for InfluxDB line protocol
string_wrapper_tag = lambda s: str(s)
string_wrapper = lambda s: "\"{}\"".format(s)
int_wrapper = lambda s: "{}i".format(int(s))
float_wrapper = lambda s: str(s)
type_converters = {
    'area': string_wrapper_tag,
    'position_name': string_wrapper_tag,
    'station_code': string_wrapper_tag,
    'so2': int_wrapper,
    'pm10': int_wrapper,
    'aqi': int_wrapper,
    'o3': int_wrapper,
    'quality': string_wrapper,
    'pm2_5': int_wrapper,
    'no2': int_wrapper,
    'co': float_wrapper,
    'primary_pollutant': string_wrapper,
}
filter_zeros = True

# program
for city in cities:
    payload['city'] = city
    r = requests.get(endpoint, params=payload, headers=headers)
    j = r.json()
    if r.status_code != requests.codes.ok or error_indicator in j:
        # got some error
        print("Request failed for city: {}".format(city), file=sys.stderr)
        print("Response code: {}".format(r.status_code), file=sys.stderr)
        pprint.PrettyPrinter(indent=4, stream=sys.stderr).pprint(j)
    else:
        for point in j:
            # filter zeros
            if filter_zeros and all(value == 0 for _, value in {key:point[key] for key in station_fields}.items()):
                print("Data error for city: {} point: {}|{}".format(city, point['station_code'], point['position_name']), file=sys.stderr)
                continue
            # get time
            timestamp = int(time.mktime(time.strptime(point[station_time], '%Y-%m-%dT%H:%M:%SZ'))  * 1000000000)
            # construct tags
            tags = ','.join(['='.join([key, type_converters[key](value)]) for key, value in {key:point[key] for key in station_tags}.items()])
            # construct datapoints
            data = ','.join(['='.join([key, type_converters[key](value)]) for key, value in {key:point[key] for key in station_fields}.items()])
            # print as InfluxDB line protocol
            # https://docs.influxdata.com/influxdb/v1.1/write_protocols/line_protocol_reference/
            infline = "{},{} {} {}".format(measurement_name, tags, data, timestamp)
            print(infline)
