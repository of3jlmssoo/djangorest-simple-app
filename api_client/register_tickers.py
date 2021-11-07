"""
export DJA_UI='admin'
export DJA_PW='amincs8000'

"""

import os
import subprocess
import coreapi

# print(os.environ['DJA_UI'])
# print(os.environ['DJA_PW'])

auth = coreapi.auth.BasicAuthentication(

    username=os.environ['DJA_UI'],
    password=os.environ['DJA_PW']
)
client = coreapi.Client(auth=auth)

print(f'{client=}')

schema = client.get('http://127.0.0.1:8000/')
print(f'{schema=}')
