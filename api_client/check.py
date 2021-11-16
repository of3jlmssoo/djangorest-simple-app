"""
export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'

200 OK
201 Created
204 No Content => deleted
400 Bad Request

"""
import json
import logging
import os
import subprocess
import unittest

import requests
from django.test import TestCase

import client_requests
from resultenum import expected_result, http_result

# DJA_UI = os.environ['DJA_UI']
# DJA_PW = os.environ['DJA_PW']
# DJA_URL = os.environ['DJA_URL']


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


class ApiTest4Ticker(TestCase):

    def __init__(self, *args, **kwargs):
        print(f'ApiTest')
        super().__init__(*args, **kwargs)
        self.DJA_UI = os.environ['DJA_UI']
        self.DJA_PW = os.environ['DJA_PW']
        self.DJA_URL = os.environ['DJA_URL']
        self.content_type = {'content-type': 'application/json'}
        self.app = 'tickers'
        # self.session = requests.Session()
        # self.session.auth = (DJA_UI, DJA_PW)
        # self.headers = {'content-type': 'application/json'}

        self.client_requests = client_requests.client_requests(
            self.DJA_UI,
            self.DJA_PW,
            self.DJA_URL,
            self.content_type,
            self.app)
        # r = s.get(DJA_URL)
        # r = self.session.get(DJA_URL + 'tickers/', headers=self.headers)
        # if r.text != '[]':
        #     # print(r.text)
        #     # jtext = json.loads(r.text)
        #     # jtext
        #     print('---------------------------------------')
        #     print('--- please delete the existing data ---')
        #     print('---------------------------------------')
        #     self.delete_all_data()

    # def delete_all_data(self):

    #     r = self.session.get(DJA_URL + 'tickers/', headers=self.headers)
    #     while r.text != '[]':
    #         # ret_ticker = json.loads(r.text)
    #         # id = ret_ticker[0].pop('id')
    #         # ret_ticker = json.loads(r.text)
    #         id = json.loads(r.text)[0].pop('id')
    #         logger.debug(f'{r.text} and {id=} will be deleted')
    #         self.delete_data(id)
    #         r = self.session.get(DJA_URL + 'tickers/', headers=self.headers)
    #     # print(f'{r.status_code=}')
    #     # print(f'{r.text=}')

    # def delete_data(self, id):
    #     logger.debug(f'delete_data called.  {id=}')
    #     r = self.session.delete(DJA_URL +
    #                             'tickers/' +
    #                             str(id) +
    #                             '/', headers=self.headers)

    def test_ticker(self):
        """
        - status_codeとデータ内容確認
        - 銘柄登録x1 tickerのみ
        - 銘柄登録x1 vol1, vol2, accum
        - 銘柄登録x1 ticker, vol1, vol2, accum
        - 銘柄登録x1 type(ticker) == int
        - 銘柄登録x1 vol1 = -1
        - 銘柄登録x1 vol2 = -1
        - 銘柄登録x1 accum = -1

        - put

        - 銘柄登録x2
        - 銘柄照会(全)
        - 銘柄照会x1(#1) & 銘柄照会x1(#2)
        - 銘柄削除x1(#1) & 銘柄削除x1(#2)
        """
        # - status_codeとデータ内容確認
        # - 銘柄登録x1 tickerのみ
        #####################################################################
        logger.debug(f'1) 銘柄登録x1 tickerのみ')
        ticker_code = 'mc'
        params = {'ticker': ticker_code}
        # result, r = self.client_requests.post_data(ticker_code, params)
        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(f'     when post, unexpected status:{r.status_code=}')
            # return
        logger.debug(f'     post. {r.status_code=} {r.text=}')
        ret_ticker = json.loads(r.text)  # POSTでr.textにデータがセットされる
        id = ret_ticker.pop('id')
        ref_ticker = {
            'ticker': ticker_code,
            'vol1': 0,
            'vol2': 0,
            'accum': 0,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)

        # GET(query)
        result, r = self.client_requests.get_data(ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        ret_ticker = json.loads(r.text)
        ret_ticker = ret_ticker[0]
        id = ret_ticker.pop('id')

        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=} {id=} {ticker_code=}.')

        # DELETE
        result, r = self.client_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when get, unexpected status:{r.status_code=}')
            return
        # ref_code = 204
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)
        logger.debug(f'     delete.  {r.status_code=} {id=}.')
        logger.debug(f'1) 銘柄登録x1 tickerのみ')

        #####################################################################
        logger.debug(f'2) 銘柄登録x1 vol1, vol2, accum')
        # ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
        ref_code = 400
        params = {
            # 'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}

        # result, r = self.client_requests.post_data(ticker_code, params)
        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(http_result.BadRequest.value, r.status_code)

        logger.debug(f'2) 銘柄登録x1 vol1, vol2, accum')

        #####################################################################
        logger.debug(f'3) 銘柄登録x1 ticker, vol1, vol2, accum')
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
        # ref_code = 201
        ref_code = http_result.Created.value
        params = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        # POST
        # r = self.session.post(
        #     DJA_URL + 'tickers/',
        #     data=json.dumps(params),
        #     headers=self.headers)
        # result, r = self.client_requests.post_data(ticker_code, params)
        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        ret_ticker = json.loads(r.text)  # POSTでr.textにデータがセットされる
        id = ret_ticker.pop('id')
        ref_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)

        # GET(query)
        ref_code = http_result.OK.value
        result, r = self.client_requests.get_data(ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        ret_ticker = json.loads(r.text)
        ret_ticker = ret_ticker[0]
        id = ret_ticker.pop('id')
        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(f'     get(query).  {r.status_code=} {ticker_code=}.')

        # DELETE
        result, r = self.client_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when get, unexpected status:{r.status_code=}')
            return
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)

        logger.debug(f'3) 銘柄登録x1 ticker, vol1, vol2, accum')

        #####################################################################
        logger.debug(f'4) 銘柄登録x1 type(ticker) == int (int2str)')
        ticker_code = 123
        ref_code = 201
        params = {'ticker': ticker_code}
        # POST
        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return
        ret_ticker = json.loads(r.text)  # POSTでr.textにデータがセットされる
        id = ret_ticker.pop('id')
        ref_ticker = {
            'ticker': str(ticker_code),  # 自動でstr化される
            'vol1': 0,
            'vol2': 0,
            'accum': 0,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)
        # GET(query)
        # ref_code = 200
        result, r = self.client_requests.get_data(
            str(ticker_code))  # need to convert to string from int
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        ret_ticker = json.loads(r.text)
        ret_ticker = ret_ticker[0]
        id = ret_ticker.pop('id')

        self.assertEqual(ref_ticker, ret_ticker)

        # r = self.session.get(
        #     DJA_URL +
        #     'tickersname/?ticker=' +
        #     str(ticker_code),
        #     headers=self.headers)
        # ref_data = {'status_code': ref_code, 'ticker': ref_ticker}
        # ret_ticker = json.loads(r.text)
        # id = ret_ticker[0].pop('id')
        # ret_data.clear()
        # ret_data = {'status_code': r.status_code, 'ticker': ret_ticker[0]}
        # logger.debug(f'     {ret_data=} {type(ret_data)=}')
        # logger.debug(f'     {ref_data=} {type(ref_data)=}')
        # self.assertEqual(ref_data, ret_data)
        # logger.debug(f'     get(query).  {r.status_code=} {ticker_code=}.')
        # ret_ticker = json.loads(r.text)
        # id = ret_ticker[0].pop('id')

        # DELETE
        result, r = self.client_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when get, unexpected status:{r.status_code=}')
            return
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)
        logger.debug(f'     delete.  {r.status_code=} {id=}.')

        # ref_code = 204
        # r = self.session.delete(DJA_URL +
        #                         'tickers/' +
        #                         str(id) +
        #                         '/', headers=self.headers)
        # self.assertEqual(ref_code, r.status_code)
        # logger.debug(f'     delete.  {r.status_code=} {id=}.')

        logger.debug(f'4) 銘柄登録x1 type(ticker) == int')

        logger.debug(f'5) 銘柄登録x1 vol1 = -1')
        ticker_code = 'mc'
        ticker_vol1 = -1
        ticker_vol2 = 3
        ticker_accum = 100
        ref_code = http_result.BadRequest.value
        params = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(ref_code, r.status_code)

        logger.debug(f'5) 銘柄登録x1 vol1 = -1')

        logger.debug(f'6) 銘柄登録x1 vol2 = -1')
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = -2
        ticker_accum = 100
        ref_code = http_result.BadRequest.value
        params = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(ref_code, r.status_code)

        logger.debug(f'6) 銘柄登録x1 vol2 = -1')

        logger.debug(f'7) 銘柄登録x1 accum = -1')
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = -3
        ticker_accum = -100
        ref_code = http_result.BadRequest.value
        params = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(ref_code, r.status_code)

        logger.debug(f'7) 銘柄登録x1 accum = -1')

        logger.debug(f'8) put')
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
        # ref_code = 201
        ref_code = http_result.Created.value
        params = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        ret_ticker = json.loads(r.text)  # POSTでr.textにデータがセットされる
        id = ret_ticker.pop('id')
        ref_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)

        # GET(query)
        result, r = self.client_requests.get_data(ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        ret_ticker = json.loads(r.text)
        ret_ticker = ret_ticker[0]
        id = ret_ticker.pop('id')

        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=} {id=} {ticker_code=}.')

        # PUT
        logger.debug(f'===> {ret_ticker=}')
        for k in ret_ticker.keys():
            print(k)
        # {ret_ticker[ticker]=}')
        logger.debug(f'===> {ret_ticker=} {type(ret_ticker)=}')
        logger.debug(f'===> {ret_ticker["ticker"]=}')
        params = {
            'ticker': ret_ticker['ticker'],
            'vol1': 500,
            # 'vol2': ret_ticker['vol2'],
            # 'accum': ret_ticker['accum']
        }
        result, r = self.client_requests.put_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        logger.debug(f'     {r.status_code=} {r.text=}')

        # GET(query)
        result, r = self.client_requests.get_data(ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        ret_ticker = json.loads(r.text)
        ret_ticker = ret_ticker[0]
        id = ret_ticker.pop('id')

        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=} {id=} {ticker_code=} {r.text=}')

        logger.debug(f'8) put')

        print(f'===========================================')

        # - 銘柄登録x2
        # - 銘柄照会(全)
        # - 銘柄照会x1(#1) & 銘柄照会x1(#2)
        # - 銘柄削除x1(#1) & 銘柄削除x1(#2)

        # params = {'ticker': 'mc'}
        # r = self.session.post(
        #     DJA_URL + 'tickers/',
        #     data=json.dumps(params),
        #     headers=self.headers)

        # print(f'{r.status_code=}')
        # print(f'{r.json=}')
        # print(f'{type(r.json)=}')
        # print(f'{r.text=}')
        # print(f'{type(r.text)=}')
        # jtext = json.loads(r.text)
        # print(f'{type(jtext)=}')

        # params = {'ticker': 'mss'}
        # r = self.session.post(
        #     DJA_URL + 'tickers/',
        #     data=json.dumps(params),
        #     headers=self.headers)

        # r = self.session.get(DJA_URL + 'tickers/', headers=self.headers)
        # print(r.text)
        # jtext = json.loads(r.text)
        # jtext

        # r = self.session.get(
        #     DJA_URL +
        #     'tickersname/?ticker=mc',
        #     headers=self.headers)
        # print(r.text)
        # jtext = json.loads(r.text)
        # jtext
        # r = self.session.delete(DJA_URL +
        #                         'tickers/' +
        #                         str(jtext[0]['id']) +
        #                         '/', headers=self.headers)
        # print(f'{r.status_code=}')
        # print(f'{r.text=}')

        # r = self.session.get(
        #     DJA_URL +
        #     'tickersname/?ticker=mss',
        #     headers=self.headers)
        # print(r.text)
        # jtext = json.loads(r.text)
        # jtext

        # r = self.session.delete(DJA_URL +
        #                         'tickers/' +
        #                         str(jtext[0]['id']) +
        #                         '/', headers=self.headers)
        # print(f'{r.status_code=}')
        # print(f'{r.text=}')


test = ApiTest4Ticker()
test.test_ticker()
