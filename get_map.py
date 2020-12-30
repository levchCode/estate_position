import urllib.request
import pandas as pd
import time
import random


def save_fragment(filename, lon, lng):
    URL = "http://static-maps.yandex.ru/1.x/?ll={0},{1}&pt={0},{1}&spn=0.0027,0.0027&l=map".format(lon, lng)
    urllib.request.urlretrieve(URL, filename + ".png")