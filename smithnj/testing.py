import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import pandas as pd
import geopandas

RIDERSHIP_STATS = pd.read_json('http://data.cityofchicago.org/resource/5neh-572f.json') #TODO Change from https to http
print('grabbed ridership')
NEIGHBORHOODS = geopandas.read_file('http://data.cityofchicago.org/api/geospatial/bbvz-uum9?method=export&format=GeoJSON') #TODO Change file to use geopandas + http, update README and fix link
print('grabbed neigh')
CENSUS = pd.read_json('http://data.cityofchicago.org/resource/kn9c-c2s2.json') #TODO Change from https to http
print('grabbed census')
LOCATIONS = geopandas.read_file('http://datamechanics.io/data/smithnj/CTA_RailStations.geojson') #TODO Change file to use goepandas, update README
print('grabbed locations')
CONGESTION = pd.read_json('https://data.cityofchicago.org/resource/m65n-ux8y.json') #TODO Get rid of previous dataset in both grabfiles
print('grabbed congestion')

#  ALL_DATA = [RIDERSHIP_STATS, NEIGHBORHOODS, CENSUS, INCOME, LOCATIONS]
ALL_DATA = [RIDERSHIP_STATS, NEIGHBORHOODS, CENSUS, LOCATIONS, CONGESTION]

print('RIDERSHIP')
print(list(RIDERSHIP_STATS))
print('NEIGH')
print(list(NEIGHBORHOODS))
print('CENSUS')
print(list(CENSUS))
print('LOCATIONS')
print(list(LOCATIONS))
print('CONGESTION')
print(list(CONGESTION))