#!/usr/bin/env python3

import time
import datetime
import requests
import json
import sys

url = """http://www.hzctrc.com/arcgis/rest/services/V32/webtraffic_bck/MapServer/identify?f=json&geometry=%s&tolerance=1&returnGeometry=false&mapExtent={"xmin":120.000,"ymin":30.000,"xmax":121.000,"ymax":31.000,"spatialReference":{"wkid":4326}}&imageDisplay=400,400,96&geometryType=esriGeometryEnvelope&sr=4326&layers=all:0,1,2,3,4,5"""
dataset = "webtraffic_bck"

#                     xmin        ymin   xmax   ymax
r = requests.get(url %"122.040,30.265,120.150,30.313")

if len(r.json()['results']) == 0:
    print("Server sent no data", file=sys.stderr)
    sys.exit(1)

# print(r.content.decode("utf-8"))
for data in r.json()['results']:
    print("{},id={},objectid={},rank={},fnode={},tnode={} status={},speed={} {}".format(
            dataset,
            data['attributes']['ID'],
            data['attributes']['OBJECTID'],
            data['attributes']['RANK'],
            data['attributes']['FNODE_'],
            data['attributes']['TNODE_'],
            data['attributes']['ZHUANGTAI'],
            data['attributes']['SPEED'],
            int(datetime.datetime.now().timestamp() * 1000000000)
        ))


print("success lines:%s" %len(r.json()['results']), datetime.datetime.now(), file=sys.stderr)
