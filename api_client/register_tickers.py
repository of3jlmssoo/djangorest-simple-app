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

import csv
import json
import logging
import os
import sys

import requests

from client_requests import client_requests
from refs import DEFAULT_DIR, PORTFOLIO_FILE1, PORTFOLIO_FILE2

# import subprocess


logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.propagate = False
# DEBUG INFO WARNIG ERROR CRTICAL
logger.setLevel(logging.DEBUG)
ch.setLevel(logging.DEBUG)
logger.disabled = False


class RegisterTicker(object):

    def __init__(self, *args, **kwargs):
        print('ApiTest')
        super().__init__(*args, **kwargs)
        self.DJA_UI = os.environ['DJA_UI']
        self.DJA_PW = os.environ['DJA_PW']
        self.DJA_URL = os.environ['DJA_URL']
        self.content_type = {'content-type': 'application/json'}

        self.app = 'tickers'
        self.ticker_requests = client_requests(
            self.DJA_UI,
            self.DJA_PW,
            self.DJA_URL,
            self.content_type,
            self.app)

        self.app = 'dividends'
        self.dividend_requests = client_requests(
            self.DJA_UI,
            self.DJA_PW,
            self.DJA_URL,
            self.content_type,
            self.app)

    def read_csv(self):
        f_list = [DEFAULT_DIR + PORTFOLIO_FILE1, DEFAULT_DIR + PORTFOLIO_FILE2]
        for i, csvf in enumerate(f_list):
            """ 'ticker', 'volume'
            """
            with open(csvf) as f:
                for row in csv.reader(f):
                    # change the type of 'volume', row[1], to int from str
                    row[1] = int(row[1])
                    self.post_patch_ticker(i, row)

    def post_patch_ticker(self, i: 0 | 1, row: list):
        vol = 'vol1' if i == 0 else 'vol2'
        # self.ticker_requests.postData({'ticker': row[0], vol: row[1]})
        # print({'ticker': row[0], vol: row[1]})
        if (resultIsExist := self.ticker_requests.isThisTickerExist(row[0])):
            result = self.ticker_requests.patchData(
                resultIsExist['id'], {vol: row[1]})
        else:
            result = self.ticker_requests.postData(
                {"ticker": row[0], vol: row[1]})
        if not result:
            print(
                f'register_tickers.post_patch_ticker error {i=} {row}. error {result=} when {"PATCH" if resultIsExist == True else "POST"}')


regtic = RegisterTicker()
regtic.read_csv()
