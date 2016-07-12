#!/usr/bin/env python3
# This converts iLiveTraffice 2.0 JSON format to InfluxDB Line Protocol.
# Input example see `sample_data/congest_index_of_net_for_date.json`
# It updates every 5 min with a 5-10 min delay.
# Output format see https://docs.influxdata.com/influxdb/v0.13/write_protocols/line/
import requests, dateutil.parser, os, sys

url = "http://115.238.43.206:8300/congest_index/congest_index_of_net_for_date.json"
dataset = "congest_index"

speed_array = requests.get(url).json()

for point in speed_array:
	print("{},net_name={},net_code={} speed={},congest_index={} {}".format(
			dataset,
			point["net_name"].replace(",", r"\,").replace(" ", r"\ "),
			point["net_code"],
			point["speed"],
			point["congest_index"],
			int(dateutil.parser.parse(point["record_date"]).timestamp()) * 1000000000
		))

