"""
まずデータをDELETEしてその上で、2つあるポートフォリオファイルの銘柄情報をPOST/PATCHで登録
CSVファイルのフォーマットは、ticker,vol
CSVファイルは2つ。1つのvolはvol1へ、もう1つのvolはvol2へ登録する

export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'
export PYTHONPATH='../:../api_client/:../client/'

print(r.url)
print(r.text)
print(r.status_code)

__init__()
read_csv()
post_patch_ticker()
"""

import csv
import logging
import os

from client_requests import client_requests
from refs import DEFAULT_DIR, PORTFOLIO_FILE1, PORTFOLIO_FILE2

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

        # djangoアクセスのための準備
        self.DJA_UI = os.environ['DJA_UI']
        self.DJA_PW = os.environ['DJA_PW']
        self.DJA_URL = os.environ['DJA_URL']
        self.content_type = {'content-type': 'application/json'}

        # REST　API準備
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

    def read_csv(self) -> None:
        """ Return Noneのままで良いか？ """

        self.dividend_requests.deleteAllData()
        self.ticker_requests.deleteAllData()

        f_list = [DEFAULT_DIR + PORTFOLIO_FILE1, DEFAULT_DIR + PORTFOLIO_FILE2]
        for i, csvf in enumerate(f_list):
            """ 想定しているcsvフォーマット : 'ticker', 'volume' """
            with open(csvf) as f:
                for row in csv.reader(f):
                    # change the type of 'volume', row[1], to int from str
                    row[1] = int(row[1])
                    self.post_patch_ticker(i, row)

    def post_patch_ticker(self, i: 0 | 1, row: list) -> None:
        """ Return Noneのままで良いか？

        1つ目のファイルはvol1にvolumeを登録し、2つ目のファイルはvol2にvolumeを登録する
        2つ目のファイルの銘柄が登録されているとは限らないのでisThisTickerExistで確認の上patchからpostする
        """
        vol = 'vol1' if i == 0 else 'vol2'
        if (resultIsExist := self.ticker_requests.isThisTickerExist(row[0])):
            result = self.ticker_requests.patchData(resultIsExist['id'], {vol: row[1]})
        else:
            result = self.ticker_requests.postData({"ticker": row[0], vol: row[1]})
        if not result:
            print(
                f'register_tickers.post_patch_ticker error {i=} {row}. error {result=} when {"PATCH" if resultIsExist == True else "POST"}')


regtic = RegisterTicker()
regtic.read_csv()
