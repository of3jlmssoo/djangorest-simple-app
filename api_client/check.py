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

        self.client_requests = client_requests.client_requests(
            self.DJA_UI,
            self.DJA_PW,
            self.DJA_URL,
            self.content_type,
            self.app)

    def test_ticker(self):
        """
        - status_codeとデータ内容確認
        - 銘柄登録x1 tickerのみ
        - 銘柄登録x1 vol1, vol2, accum(エラー)
        - 銘柄登録x1 ticker, vol1, vol2, accum
        - 銘柄登録x1 type(ticker) == int
        - 銘柄登録x1 vol1 = -1(エラー)
        - 銘柄登録x1 vol2 = -1(エラー)
        - 銘柄登録x1 accum = -1(エラー)

        - patch

        - 銘柄登録x2
        - 銘柄照会(全)
        - 銘柄照会x1(#1) & 銘柄照会x1(#2)
        - 銘柄削除x1(#1) & 銘柄削除x1(#2)
        """
        #####################################################################
        logger.debug(f'1) 銘柄登録x1 tickerのみ')

        # POST
        ticker_code = 'mc'
        params = {'ticker': ticker_code}
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

        # GET(query) with ticker code
        result, r = self.client_requests.get_data(ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        # ret_ticker = json.loads(r.text)
        # ret_ticker = ret_ticker[0]
        logger.debug(f'     GET {r.text=}')
        ret_ticker = json.loads(r.text)[0]  # POST : {}で返される。GET : [{}]で返される
        id = ret_ticker.pop('id')
        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=} {id=} {ticker_code=} {ret_ticker=}.')

        # DELETE
        result, r = self.client_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when get, unexpected status:{r.status_code=}')
            return
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)
        self.assertEqual(r.status_code, ref_code)
        logger.debug(f'     delete.  {r.status_code=} {id=}.')
        logger.debug(f'1) 銘柄登録x1 tickerのみ')

        #####################################################################
        logger.debug(f'2) 銘柄登録x1 vol1, vol2, accum(エラー)')
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
        params = {
            # 'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}

        result, r = self.client_requests.post_data(params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(http_result.BadRequest.value, r.status_code)

        logger.debug(f'2) 銘柄登録x1 vol1, vol2, accum(エラー)')

        ####################################################################
        logger.debug(f'3) 銘柄登録x1 ticker, vol1, vol2, accum')

        # POST
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
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
        ref_code = http_result.OK.value
        result, r = self.client_requests.get_data(ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        logger.debug(f'     GET {r.text=}')
        ret_ticker = json.loads(r.text)[0]
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

        # POST
        ticker_code = 123
        ref_code = http_result.Created  # 自動でstr化されるのでCreated
        params = {'ticker': ticker_code}
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
        result, r = self.client_requests.get_data(
            str(ticker_code))  # need to convert to string from int
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        ret_ticker = json.loads(r.text)[0]
        id = ret_ticker.pop('id')

        self.assertEqual(ref_ticker, ret_ticker)

        # DELETE
        result, r = self.client_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when get, unexpected status:{r.status_code=}')
            return
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)
        logger.debug(f'     delete.  {r.status_code=} {id=}.')

        logger.debug(f'4) 銘柄登録x1 type(ticker) == int')

        logger.debug(f'5) 銘柄登録x1 vol1 = -1(エラー)')
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

        logger.debug(f'5) 銘柄登録x1 vol1 = -1(エラー)')

        #####################################################################
        logger.debug(f'6) 銘柄登録x1 vol2 = -1(エラー)')
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

        logger.debug(f'6) 銘柄登録x1 vol2 = -1(エラー)')

        #####################################################################
        logger.debug(f'7) 銘柄登録x1 accum = -1(エラー)')
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

        logger.debug(f'7) 銘柄登録x1 accum = -1(エラー)')

        #####################################################################
        logger.debug(f'8) patch')

        # POST this data should be updated with patch command later
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
        ret_ticker = json.loads(r.text)[0]
        # ret_ticker = ret_ticker[0]
        id = ret_ticker.pop('id')

        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=} {id=} {ticker_code=}.')

        # PATCH
        ticker_vol1_new = 500
        ref_ticker['vol1'] = ticker_vol1_new
        params['vol1'] = ticker_vol1_new
        result, r = self.client_requests.patch_data(id, params)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when patch, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        logger.debug(f'     {r.status_code=} {r.text=}')

        # GET(query)
        result, r = self.client_requests.get_data(ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        ret_ticker = json.loads(r.text)[0]
        id = ret_ticker.pop('id')

        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=}  {r.text=}')

        logger.debug(f'8) put')

        #####################################################################
        # # - 銘柄登録x2
        print(f'===========================================')
        #####################################################################
        # # - 銘柄照会(全)
        print(f'===========================================')
        #####################################################################
        # # - 銘柄照会x1(#1) & 銘柄照会x1(#2)
        print(f'===========================================')
        #####################################################################
        # # - 銘柄削除x1(#1) & 銘柄削除x1(#2)
        print(f'===========================================')


test = ApiTest4Ticker()
test.test_ticker()
