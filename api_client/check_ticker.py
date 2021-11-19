"""
export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'

200 OK
201 Created
204 No Content => deleted
400 Bad Request

"""
# import json
import logging
import os

# import requests
from django.test import TestCase

from client_requests import client_requests
from resultenum import expected_result, http_result

# import subprocess
# import unittest


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
        """
        """ ########### TODO: replace with isThisExist ############ """
        logger.debug('0) delete_all_data')
        # DELETE
        r = self.dividend_requests.session.get(
            self.DJA_URL + 'dividends/', headers=self.content_type)
        logger.debug(f'dividend {r.text=}')
        if r.text != '[]':
            self.dividend_requests.delete_all_data()
        r = self.dividend_requests.session.get(
            self.DJA_URL + 'tickers/', headers=self.content_type)
        logger.debug(f'dividend {r.text=}')
        if r.text != '[]':
            self.ticker_requests.delete_all_data()

        logger.debug('0) delete_all_data')

        """ ##################################################################### """
        logger.debug('1) 銘柄登録x1 tickerのみ')

        # POST
        ticker_code = 'mc'
        params_ticker = {'ticker': ticker_code}
        result, r = self.ticker_requests.post_data(
            params_ticker)
        if result != expected_result.as_expected:
            logger.debug(f'     when post, unexpected status:{r.status_code=}')
            # return
        logger.debug(f'     post. {r.status_code=} {r.text=}')
        id, ret_ticker = self.ticker_requests.pop_id_from_POST_data(r.text)
        ref_ticker = {
            'ticker': ticker_code,
            'vol1': 0,
            'vol2': 0,
            'accum': 0,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)

        # GET(query) with ticker code
        result, r = self.ticker_requests.get_data_of_ticker(
            ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        logger.debug(f'     GET {r.text=}')
        id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=} {id=} {ticker_code=} {ret_ticker=}.')

        # DELETE
        result, r = self.ticker_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when get, unexpected status:{r.status_code=}')
            return
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)
        logger.debug(f'     delete.  {r.status_code=} {id=}.')
        logger.debug('1) 銘柄登録x1 tickerのみ')

        """ ##################################################################### """
        logger.debug('2) 銘柄登録x1 vol1, vol2, accum(エラー)')
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
        params_ticker = {
            # 'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}

        result, r = self.ticker_requests.post_data(params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(http_result.BadRequest.value, r.status_code)

        logger.debug('2) 銘柄登録x1 vol1, vol2, accum(エラー)')

        """ ##################################################################### """
        logger.debug('3) 銘柄登録x1 ticker, vol1, vol2, accum')

        # POST
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
        ref_code = http_result.Created.value
        params_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.ticker_requests.post_data(params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return
        logger.debug(f'     post. {r.status_code=} {r.text=}')
        id, ret_ticker = self.ticker_requests.pop_id_from_POST_data(r.text)
        ref_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)

        # GET(query)
        ref_code = http_result.OK.value
        result, r = self.ticker_requests.get_data_of_ticker(
            ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        logger.debug(f'     GET {r.text=}')
        id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(f'     get(query).  {r.status_code=} {ticker_code=}.')

        # DELETE
        result, r = self.ticker_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when get, unexpected status:{r.status_code=}')
            return
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)

        logger.debug('3) 銘柄登録x1 ticker, vol1, vol2, accum')

        """ #################################################################### """
        logger.debug('4) 銘柄登録x1 type(ticker) == int (int2str)')

        # POST
        ticker_code = 123
        ref_code = http_result.Created  # 自動でstr化されるのでCreated
        params_ticker = {'ticker': ticker_code}
        result, r = self.ticker_requests.post_data(params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return
        id, ret_ticker = self.ticker_requests.pop_id_from_POST_data(r.text)
        ref_ticker = {
            'ticker': str(ticker_code),  # 自動でstr化される
            'vol1': 0,
            'vol2': 0,
            'accum': 0,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)

        # GET(query)
        result, r = self.ticker_requests.get_data_of_ticker(
            str(ticker_code))  # need to convert to string from int
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
        self.assertEqual(ref_ticker, ret_ticker)

        # DELETE
        result, r = self.ticker_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when get, unexpected status:{r.status_code=}')
            return
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)
        logger.debug(f'     delete.  {r.status_code=} {id=}.')

        logger.debug('4) 銘柄登録x1 type(ticker) == int')

        logger.debug('5) 銘柄登録x1 vol1 = -1(エラー)')
        ticker_code = 'mc'
        ticker_vol1 = -1
        ticker_vol2 = 3
        ticker_accum = 100
        ref_code = http_result.BadRequest.value
        params_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.ticker_requests.post_data(params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(ref_code, r.status_code)

        logger.debug('5) 銘柄登録x1 vol1 = -1(エラー)')

        """ ##################################################################### """
        logger.debug('6) 銘柄登録x1 vol2 = -1(エラー)')
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = -2
        ticker_accum = 100
        ref_code = http_result.BadRequest.value
        params_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.ticker_requests.post_data(params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(ref_code, r.status_code)

        logger.debug('6) 銘柄登録x1 vol2 = -1(エラー)')

        """ ##################################################################### """
        logger.debug('7) 銘柄登録x1 accum = -1(エラー)')
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = -3
        ticker_accum = -100
        ref_code = http_result.BadRequest.value
        params_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.ticker_requests.post_data(params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        self.assertEqual(ref_code, r.status_code)

        logger.debug('7) 銘柄登録x1 accum = -1(エラー)')

        """ ##################################################################### """
        logger.debug('8) patch')

        # POST this data should be updated with patch command later
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
        # ref_code = 201
        ref_code = http_result.Created.value
        params_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.ticker_requests.post_data(params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return

        logger.debug(f'     post. {r.status_code=} {r.text=}')
        id, ret_ticker = self.ticker_requests.pop_id_from_POST_data(r.text)
        ref_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)

        # GET(query)
        result, r = self.ticker_requests.get_data_of_ticker(
            ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=} {id=} {ticker_code=}.')

        # PATCH
        ticker_vol1_new = 500
        ref_ticker['vol1'] = ticker_vol1_new
        params_ticker['vol1'] = ticker_vol1_new
        result, r = self.ticker_requests.patch_data(
            id, params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when patch, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        logger.debug(f'     {r.status_code=} {r.text=}')

        # GET(query)
        result, r = self.ticker_requests.get_data_of_ticker(
            ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
        self.assertEqual(ref_ticker, ret_ticker)
        logger.debug(
            f'     get(query).  {r.status_code=}  {r.text=}')

        logger.debug('8) put')

        """ ##################################################################### """
        logger.debug('9) put銘柄登録x2')

        result, r = self.ticker_requests.get_data_of_all()
        logger.debug(f'     {r.status_code=} {r.text=}')
        if r.text != '[]':
            print('---------------------------------------')
            print('--- please delete the existing data ---')
            print('---------------------------------------')
            self.ticker_requests.delete_all_data()

        tickers = ['mc', 'mss']

        # POST
        for ticker_code in tickers:
            # ticker_code = ticker
            params_ticker = {'ticker': ticker_code}
            result, r = self.ticker_requests.post_data(
                params_ticker)
            if result != expected_result.as_expected:
                logger.debug(
                    f'     when post, unexpected status:{r.status_code=}')
                # return
            logger.debug(f'     post. {r.status_code=} {r.text=}')
            id, ret_ticker = self.ticker_requests.pop_id_from_POST_data(r.text)
            ref_ticker = {
                'ticker': ticker_code,
                'vol1': 0,
                'vol2': 0,
                'accum': 0,
                'owner': self.DJA_UI}
            self.assertEqual(ref_ticker, ret_ticker)

        # GET(query) with ticker code
        for ticker_code in tickers:
            result, r = self.ticker_requests.get_data_of_ticker(
                ticker_code)
            if result != expected_result.as_expected:
                logger.debug(
                    f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
                # return
            logger.debug(f'     GET {r.text=}')
            id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
            ref_ticker = {
                'ticker': ticker_code,
                'vol1': 0,
                'vol2': 0,
                'accum': 0,
                'owner': self.DJA_UI}
            self.assertEqual(ref_ticker, ret_ticker)
            logger.debug(
                f'     get(query).  {r.status_code=} {id=} {ticker_code=} {ret_ticker=}.')

        # DELETE
        result, r = self.ticker_requests.get_data_of_all()
        logger.debug(f'     before DELETE {r.text=}')

        for ticker_code in tickers:
            result, r = self.ticker_requests.get_data_of_ticker(
                ticker_code)
            if result != expected_result.as_expected:
                logger.debug(
                    f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
                # return
            logger.debug(f'     GET {r.text=}')
            id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
            result, r = self.ticker_requests.delete_data(id)
            if result != expected_result.as_expected:
                logger.debug(
                    f'     when get, unexpected status:{r.status_code=}')
                return
            ref_code = http_result.NoContentDeleted.value
            self.assertEqual(ref_code, r.status_code)
            logger.debug(f'     delete.  {r.status_code=} {id=}.')
            result, r = self.ticker_requests.get_data_of_all()
            logger.debug(f'     after DELETE {r.text=}')

        logger.debug('9) put銘柄登録x2')
        print('===========================================')

        """ ##################################################################### """
        logger.debug('10) dividend testing')

        # POST
        ticker_code = 'mc'
        ticker_vol1 = 12
        ticker_vol2 = 3
        ticker_accum = 100
        ref_code = http_result.Created.value
        params_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum}
        result, r = self.ticker_requests.post_data(params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return
        logger.debug(f'     post. {r.status_code=} {r.text=}')
        id, ret_ticker = self.ticker_requests.pop_id_from_POST_data(r.text)
        ref_ticker = {
            'ticker': ticker_code,
            'vol1': ticker_vol1,
            'vol2': ticker_vol2,
            'accum': ticker_accum,
            'owner': self.DJA_UI}
        self.assertEqual(ref_ticker, ret_ticker)

        # POST dividend
        ticker_code = 'mc'
        ex_date = '2021-11-18'
        pay_date = '2021-11-18'
        div_val = 0.12000
        div_val = '{:1.06f}'.format(0.12)
        div_rat = 3.20
        div_rat = '{:1.02f}'.format(3.2)
        ref_code = http_result.Created.value
        params_dividend = {
            'ticker': ticker_code,
            'ex_date': ex_date,
            'pay_date': pay_date,
            'div_val': div_val,
            'div_rat': div_rat,
            'owner': self.DJA_UI}
        result, r = self.dividend_requests.post_data(
            params_dividend)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when post, unexpected status:{r.status_code=} {r.text}')
            # return
        logger.debug(f'     post. {r.status_code=} {r.text=}')
        id, ret_dividend = self.ticker_requests.pop_id_from_POST_data(r.text)
        ref_dividend = {
            'ticker': ticker_code,
            'ex_date': ex_date,
            'pay_date': pay_date,
            'div_val': div_val,
            'div_rat': div_rat,
            'owner': self.DJA_UI}
        self.assertEqual(ref_dividend, ret_dividend)

        logger.debug('10) dividend testing')
        print('===========================================')


test = ApiTest4Ticker()
test.test_ticker()
