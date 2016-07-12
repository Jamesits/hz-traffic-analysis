"""
GaoDe MAP API
"""
import requests


class AMapUtil(object):
    API_KEY = '5895f97d123621945ab7003e9506806c'
    API_KEY = API_KEY
    BASE_URL = 'http://restapi.amap.com/v3/'
    GEOCODE_GEO_API = BASE_URL + 'geocode/geo'
    GEOCODE_REGEO_API = BASE_URL + 'geocode/regeo'
    BATCH_API = BASE_URL + 'batch'

    FORMAT_DATA = 'json'

    @classmethod
    def get(cls, url, data):
        data['key'] = cls.API_KEY
        data['output'] = cls.FORMAT_DATA
        req = requests.get(url, params=data)
        return req.json()

    @classmethod
    def post(cls, url, data):
        req = requests.post(url + "?key=%s" % cls.API_KEY,
                            data=data)
        return req.json()

    @classmethod
    def batch(cls, ops):
        return cls.post(url=cls.BATCH_API, data={'ops': ops})

    @classmethod
    def batch_geocode_to_address(cls, locations):
        """ locations : [[lon,lat],[lon,lat] ... ]
        最多支持批量查询20个地点
        """
        for i in range(0, len(locations), 19):
            if i + 19 < len(locations) - 1:
                data = locations[i:i + 19]
            else:
                data = locations[i:]
            location = ""
            for i in data:
                location = str(i[0]) + ',' + str(i[1]) + '|'
            location = location[:-1]
            data = {
                'location': location,
                'batch': 'true'
            }
            resp = cls.get(cls.GEOCODE_REGEO_API, data=data)
            json_resp = {}
            for regeocode in resp['regeocodes']:
                street = regeocode['addressComponent']['streetNumber']['street']
                json_resp[location] = street
            return json_resp

    @classmethod
    def geocode_to_address(cls, lon, lat):
        data = {
            'location': str(lon) + ',' + str(lat)
        }
        resp = cls.get(cls.GEOCODE_REGEO_API, data=data)
        return resp['regeocode']['addressComponent']['streetNumber']['street']

    @classmethod
    def address_to_geocode(cls, address, city=None):
        data = {
            'address': address,
            'city': city or '杭州'
        }
        resp = cls.get(cls.GEOCODE_GEO_API, data=data)
        try:
            return tuple(resp['geocodes'][0]['location'].split(','))
        except IndexError:
            return None, None
