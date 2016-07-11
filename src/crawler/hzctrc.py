#!/usr/bin/env python3

import time
import datetime
import requests
import json
url = """http://www.hzctrc.com/arcgis/rest/services/V32/webtraffic_bck/MapServer/identify?f=json&geometry=%s&tolerance=1&returnGeometry=false&mapExtent={"xmin":120.000,"ymin":30.000,"xmax":121.000,"ymax":31.000,"spatialReference":{"wkid":4326}}&imageDisplay=400,400,96&geometryType=esriGeometryEnvelope&sr=4326&layers=all:0,1,2,3,4,5"""
while (1):
    #                     xmin        ymin   xmax   ymax
    r = requests.get(url %"122.040,30.265,120.150,30.313")

    if len(r.json()['results']) == 0:
        print("Error")
        raise

    print(r.content.decode("utf-8"))
    break
    file = open("%s.json" %datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") ,"a+")
    for data in r.json()['results']:
        _data = {}
        _data['id'] = data['attributes']['ID']
        _data['rank'] = data['attributes']['RANK']
        _data['speed'] = data['attributes']['SPEED']
        _data['fnode'] = data['attributes']['FNODE_']
        _data['tnode'] = data['attributes']['TNODE_']
        _data['paths'] = data['geometry']['paths']
        file.write(json.dumps(_data))
        file.write("\n")


    file.close()

    print("success lines:%s" %len(r.json()['results']), datetime.datetime.now())

    time.sleep(60)


# {
#     'f': 'json',
#     'geometry': '120.15060743622993,30.210347717148587,120.21060743622993,30.260347717148587',
#     'geometryType': 'esriGeometryEnvelope',
#     'imageDisplay': '400,400,96',
#     'mapExtent': '{"xmin":120.13,"ymin":30.23,"xmax":120.17,"ymax":30.26,"spatialReference":{"wkid":4326}}',
#     'returnGeometry': True,
#     'tolerance': 1}








# for data in datas['results']:
#     _data = {}
#     _data['id'] = data['attributes']['ID']
#     _data['rank'] = data['attributes']['RANK']
#     _data['speed'] = data['attributes']['SPEED']
#     _data['fnode'] = data['attributes']['FNODE_']
#     _data['tnode'] = data['attributes']['TNODE_']
#     _data['paths'] = data['geometry']['paths']
#     r.set(_data['fnode']+":"+_data['tnode'], _data)



# for data in speed_datas:
#     for road in data['finegrit']:
#         f.write("{0}->{1} ID#{2}".format(road['t#from_node_id'], road['t#to_node_id'],road['t#link_id']))
#         f.write("\n")
#         f.write(str(r.exists("{0}:{1}".format(road['t#from_node_id'],road['t#to_node_id']))))
#         f.write("\n")

