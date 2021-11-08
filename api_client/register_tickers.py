"""
POST
GET
PATCH (update)
DELETE
PUT(???)


export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'

print(r.url)
print(r.text)
print(r.status_code)
"""

import json
import os
import subprocess

import requests

DJA_UI = os.environ['DJA_UI']
DJA_PW = os.environ['DJA_PW']
DJA_URL = os.environ['DJA_URL']

s = requests.Session()
s.auth = (DJA_UI, DJA_PW)
r = s.get(DJA_URL)

headers = {'content-type': 'application/json'}
params = {'ticker': 'mc'}
r = s.post(DJA_URL + 'tickers/', data=json.dumps(params), headers=headers)
print(r.status_code)
print(r.json)
