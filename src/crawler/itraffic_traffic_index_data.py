#!/usr/bin/env python3
# This converts iLiveTraffice 2.0 JSON format to InfluxDB Line Protocol.
# Input example see `sample_data/traffic_index_data_for_date.json`
# It updates every 5 min with a 5-10 min delay.
# Output format see https://docs.influxdata.com/influxdb/v0.13/write_protocols/line/
import requests, dateutil.parser, os, sys

url = "http://115.238.43.206:8300/traffic_index/traffic_index_data_for_date.json"
dataset = "traffic_index"

speed_array = requests.get(url).json()

for point in speed_array:
	try:
		data, unit = point["index_value"].split()
		unit = " (" + unit + ")"
	except ValueError:
		data = float(point["index_value"])
		unit = ""
	print("{},id={},index_name={} index_value={} {}".format(
			dataset,
			point["id"],
			(point["index_name"] + unit).replace(",", r"\,").replace(" ", r"\ "),
			data,
			int(dateutil.parser.parse(point["record_date"]).timestamp()) * 1000000000
		))
