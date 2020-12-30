import requests
import json
import time
from random import randint


def get_coords(region, addr):
    if "г," in region:
        addr = region + " " + addr
    time.sleep(randint(1, 2))
    j = requests.get("http://search.maps.sputnik.ru/search/addr?q={0}".format(addr)).content
    resp = json.loads(j)
    if "address" in resp["result"]:
        return resp["result"]["address"][0]["features"][0]["geometry"]["geometries"][0]["coordinates"][1], resp["result"]["address"][0]["features"][0]["geometry"]["geometries"][0]["coordinates"][0]
    else:
        return [0, 0]