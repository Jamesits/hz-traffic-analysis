#!/usr/bin/env python3
# This converts iTraffic JSON format to InfluxDB Line Protocol.
# Input example see `sample_data/main_road_speed_for_date.json`
# It updates every 5 min with a 5-10 min delay.
# Output format see https://docs.influxdata.com/influxdb/v0.13/write_protocols/line/
import requests, dateutil.parser, os, sys

url = "http://115.238.43.206:8300/main_road_speed/main_road_speed_for_date.json?level=3"
dataset = "speed"
persist_status_file = "/tmp/itraffic_crawler_status.tmp"

last_crawl_time = 0
try:
	with open(persist_status_file, "r") as f:
		last_crawl_time = int(f.readline())
except (IOError, ValueError):
	print("Status file not found.", file=sys.stderr)

speed_array = requests.get(url).json()
last_update_time = int(dateutil.parser.parse(speed_array[0]["record_date"]).timestamp()) * 1000000000 # InfluxDB requires timestamp in ns
if last_update_time <= last_crawl_time: sys.exit()
for point in speed_array:
	print("{},road_name={},road_class={} speed={} {}".format(
			dataset,
			point["road_name"].replace(",", r"\,").replace(" ", r"\ "),
			point["road_class"],
			point["speed"],
			last_update_time
		))

try:
	with open(persist_status_file, "w") as f:
		print(last_update_time, file=f)
except IOError:
	pass