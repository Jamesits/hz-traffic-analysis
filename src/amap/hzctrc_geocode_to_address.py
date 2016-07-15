import json

import requests

from src.amap.utils import AMapUtil

HZCTRC_API = 'http://www.hzctrc.com/arcgis/rest/services/V32/webtraffic_bck/MapServer/identify'
params = {
    'f': 'json',
    'geometry': "122.040,30.265,120.150,30.313",
    'tolerance': 1,
    'returnGeometry': 'true',
    'mapExtent': '{"xmin":120.000,"ymin":30.000,"xmax":121.000,"ymax":31.000,"spatialReference":{"wkid":4326}}',
    'imageDisplay': '400,400,96',
    'geometryType': 'esriGeometryEnvelope',
    'sr': 4326,
    'layers': 'all:0,1,2,3,4,5'
}

resp = requests.get(HZCTRC_API, params=params)
json_dict = {}
for data in resp.json()['results']:
    for path in data['geometry']['paths']:
        maps = AMapUtil.batch_geocode_to_address(path)
        print(maps)
        json_dict.update(maps)

with open('geocode_street_map.json', 'w') as jsonfile:
    json.dump(json_dict, jsonfile)
