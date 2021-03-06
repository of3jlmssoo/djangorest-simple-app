"""
export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'
export PYTHONPATH='../:../api_client/:../client/'

200 OK
201 Created
204 No Content => deleted
400 Bad Request

"""
import json
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
)
test.test_ticker1()
test.test_isThisTickerExist()
test.test_isThisIdExist()
test.test_new_postData_getAllData()
test.test_not_exist()
test.test_post_patch()
test.test_delete(
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

    def test_tickerOthers(self):
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
        result, r = self.ticker_requests.getDataOfTicker(
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
            logger.debug(f'     when delete_data, unexpected status:{r.status_code=}')
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
        result, r = self.ticker_requests.getDataOfTicker(
            str(ticker_code))  # need to convert to string from int
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
        self.assertEqual(ref_ticker, ret_ticker)
        self.assertEqual(type(id), int)
        """ id NoneかもしれないPROBLEMSについてはint型であることを確認しているので良しとする """

        # DELETE
        result, r = self.ticker_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when delete_data, unexpected status:{r.status_code=}')
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
        result, r = self.ticker_requests.getDataOfTicker(
            ticker_code)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
        self.assertEqual(ref_ticker, ret_ticker)
        self.assertEqual(type(id), int)
        """ id NoneかもしれないPROBLEMSについてはint型であることを確認しているので良しとする """

        logger.debug(f'     get(query).  {r.status_code=} {id=} {ticker_code=}.')

        # PATCH
        ticker_vol1_new = 500
        ref_ticker['vol1'] = ticker_vol1_new
        params_ticker['vol1'] = ticker_vol1_new
        result, r = self.ticker_requests.patch_data(id, params_ticker)
        if result != expected_result.as_expected:
            logger.debug(
                f'     when patch, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
            # return
        logger.debug(f'     {r.status_code=} {r.text=}')

        # GET(query)
        result, r = self.ticker_requests.getDataOfTicker(
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
            result, r = self.ticker_requests.getDataOfTicker(
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
            result, r = self.ticker_requests.getDataOfTicker(
                ticker_code)
            if result != expected_result.as_expected:
                logger.debug(
                    f'     when get, unexpected status:{r.status_code=} {result=} {expected_result.as_expected=}')
                # return
            logger.debug(f'     GET {r.text=}')
            id, ret_ticker = self.ticker_requests.pop_id_from_GET_data(r.text)
            self.assertEqual(type(id), int)
            """ id NoneかもしれないPROBLEMSについてはint型であることを確認しているので良しとする """
            result, r = self.ticker_requests.delete_data(id)
            if result != expected_result.as_expected:
                logger.debug(
                    f'     when delete_data, unexpected status:{r.status_code=}')
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

    def test_isThisTickerExist(self):
        """ ##################################################################### """

        logger.debug('11) isThisTickerExist')
        result, r = self.ticker_requests.post_data({'ticker': 'mc'})
        if result != expected_result.as_expected:
            logger.debug(f'     when post, unexpected status:{r.status_code=}')

        self.assertNotEqual(self.ticker_requests.isThisTickerExist('mc'), None)
        self.assertEqual(self.ticker_requests.isThisTickerExist('mss'), None)

        print(f'{self.ticker_requests.getAllData()=}')
        self.ticker_requests.delete_all_data()

        self.assertEqual(self.ticker_requests.isThisTickerExist('mc'), None)
        self.assertEqual(self.ticker_requests.isThisTickerExist('mss'), None)
        logger.debug('11) isThisTickerExist')

    def test_isThisIdExist(self):
        """ ##################################################################### """

        logger.debug('11-2) isThisIdExist')
        self.ticker_requests.delete_all_data()
        result = self.ticker_requests.postData({'ticker': 'mc'})
        self.assertNotEqual(result, None)
        print('check_ticker.test_isThisIdExist ticker posted correctly')
        id = self.ticker_requests.getIdOfTicker('mc')
        self.assertEqual(type(id), int)
        """ id NoneかもしれないPROBLEMSについてはint型であることを確認しているので良しとする """
        result = self.ticker_requests.isThisTickerExist(id)
        self.assertEqual(type(result), dict)

        logger.debug('11-2) isThisIdExist')

    def test_new_postData_getAllData(self):
        """ ##################################################################### """
        logger.debug('12) postData_getAllData')

        if not self.ticker_requests.postData({'ticker': 'mc'}):
            print('12) postData_getAllData error when posting mc')
        result = self.ticker_requests.getAllData()
        if result is not None:
            self.assertEqual(type(result), list)
            self.assertEqual(len(result), 1)
            self.assertEqual(len(result[0]), 6)
        else:
            print('check_ticker.test_new_postData_getAllData failed with getAllData()')

        if not self.ticker_requests.postData({'ticker': 'mss'}):
            print('12) postData_getAllData error when posting mss')

        result = self.ticker_requests.getAllData()
        if result is not None:
            self.assertEqual(type(result), list)
            self.assertEqual(len(result), 2)
            self.assertEqual(len(result[0]), 6)
            self.assertEqual(len(result[1]), 6)
        else:
            print('check_ticker.test_new_postData_getAllData failed with getAllData()')

        result = self.ticker_requests.getAllData()
        id = self.ticker_requests.getIdOfTicker("mc")
        self.assertEqual(type(id), int)
        """ id NoneかもしれないPROBLEMSについてはint型であることを確認しているので良しとする """
        if (result := self.ticker_requests.patchData(id, {"vol1": 100})):
            self.assertEqual(result["vol1"], 100)
        else:
            print('patch requeted but failed')
            print(f'{self.ticker_requests.getAllData()=}')

        self.ticker_requests.delete_all_data()
        logger.debug('12) postData_getAllData')

    def test_not_exist(self):
        """ ##################################################################### """
        logger.debug('13) not exist')
        self.ticker_requests.delete_all_data()

        result = self.ticker_requests.isThisTickerExist('mc')
        self.assertEqual(result, None)

        result = self.ticker_requests.getAllData()
        self.assertEqual(result, None)

        result = self.ticker_requests.getIdOfTicker('mc')
        self.assertEqual(result, None)
        ###########################################
        result = self.ticker_requests.isThisTickerExist(100)
        self.assertEqual(result, None)

        # test_not_existであり、かつ、getIdOfTickerでタイプチェックしているので100のPROBLEMSは良しとする
        result = self.ticker_requests.getIdOfTicker(100)
        self.assertEqual(result, None)

        result = self.ticker_requests.patchData(123, {'vol1': 100})
        self.assertEqual(result, None)

        logger.debug('13) not exist')

    def test_post_patch(self):
        """ ##################################################################### """
        logger.debug('14) post_patch')
        self.ticker_requests.delete_all_data()
        """ いい加減なポスト """
        params = {'tcker': 'mc'}
        result = self.ticker_requests.postData(params)
        self.assertEqual(result, None)

        params = {'vol1': 100}
        result = self.ticker_requests.postData(params)
        self.assertEqual(result, None)

        """ 正しいポスト """
        params = {'ticker': 'mc'}
        result = self.ticker_requests.postData(params)
        self.assertEqual(type(result), dict)
        print(f'test_post_patch {result=}')

        """ いい加減なパッチ"""
        id = self.ticker_requests.getIdOfTicker('mc')
        self.assertEqual(type(id), int)
        """ id NoneかもしれないPROBLEMSについてはint型であることを確認しているので良しとする """

        # 存在しないIDを指定
        invalid_maker = 100
        result = self.ticker_requests.patchData(id + invalid_maker, {'vol1': 123})
        self.assertEqual(result, None)
        # 存在しないデータキーを指定
        result = self.ticker_requests.patchData(id, {'vol3': 123})
        self.assertEqual(result, None)

        """ 正しいパッチ """
        invalid_maker = 0
        result = self.ticker_requests.patchData(id + invalid_maker, {'vol1': 123})
        self.assertEqual(type(result), dict)
        print(f'check_ticker.test_post_patch {result=}')

        logger.debug('14) post_patch')

    def test_delete(self):
        """ ##################################################################### """
        logger.debug('15) delete')

        # result = self.ticker_requests.postData({'ticker': 'mc'})
        # result = self.ticker_requests.isThisTickerExist('mc')
        # self.assertEqual(result['ticker'], 'mc')
        # result = self.ticker_requests.postData({'ticker': 'mss'})
        # result = self.ticker_requests.isThisTickerExist('mss')
        # self.assertEqual(result['ticker'], 'mss')
        self.ticker_requests.delete_all_data()
        self.ticker_requests.deleteAllData()
        result = self.ticker_requests.isThisTickerExist('mc')
        self.assertEqual(result, None)
        result = self.ticker_requests.isThisTickerExist('mss')
        self.assertEqual(result, None)

        result = self.ticker_requests.postData({'ticker': 'mc'})
        id = self.ticker_requests.getIdOfTicker('mc')
        self.assertEqual(type(id), int)
        """ id NoneかもしれないPROBLEMSについてはint型であることを確認しているので良しとする """

        """ False確認なので'mc'のタイプ問題は良しとする """
        self.assertEqual(self.ticker_requests.deleteData('mc'), False)
        self.assertEqual(self.ticker_requests.deleteData(id), True)
        self.assertEqual(self.ticker_requests.deleteData(id), False)

        logger.debug('15) delete')

    def test_ticker1(self):
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
        result, r = self.ticker_requests.getDataOfTicker(
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

        self.assertEqual(type(id), int)
        """ id NoneかもしれないPROBLEMSについてはint型であることを確認しているので良しとする """

        # DELETE
        result, r = self.ticker_requests.delete_data(id)
        if result != expected_result.as_expected:
            logger.debug(f'     when delete_data, unexpected status:{r.status_code=}')
            return
        ref_code = http_result.NoContentDeleted.value
        self.assertEqual(ref_code, r.status_code)
        logger.debug(f'     delete.  {r.status_code=} {id=}.')
        logger.debug('1) 銘柄登録x1 tickerのみ')

    def test_div(self):
        """ ##################################################################### """
        logger.debug('16) 配当関連テスト')
        self.dividend_requests.deleteAllData()
        self.ticker_requests.deleteAllData()

        result = self.ticker_requests.postData({'ticker': 'mc'})
        print('mc registered')
        # id = self.ticker_requests.getIdOfTicker('mc')
        self.dividend_requests.postData({"ticker": 'mc', "ex_date": '2021-12-01',
                                        "pay_date": '2021-12-01', "div_val": 0.121, "div_rat": 3.6})
        self.dividend_requests.postData({"ticker": 'mc', "ex_date": '2021-12-12',
                                        "pay_date": '2021-12-31', "div_val": 0.121, "div_rat": 3.6})

        result = self.ticker_requests.postData({'ticker': 'mss'})
        print('mss registered')
        # id = self.ticker_requests.getIdOfTicker('mss')
        self.dividend_requests.postData({"ticker": 'mss', "ex_date": '2020-12-01',
                                        "pay_date": '2020-12-01', "div_val": 0.121, "div_rat": 3.6})

        # print(f'{self.ticker_requests.getAllData()=}')
        # print(f'{self.dividend_requests.getAllData()=}')

        print('data loaded')
        # 2020-12-01 2021-12-01 2021-12-12
        qstrs = [
            ["ex_date=2020-12-01", 1],
            ["ex_date=2021-12-01", 1],
            ["ex_date=2021-12-12", 1],
            ["ex_date__gte=2020-12-01&ex_date__lte=2021-12-01", 2],
            # ["ex_date__gte=2020-12-01&ex_date__lte=2021-12-12", 2],
            ["ex_date__gte=2021-12-01&ex_date__lte=2021-12-12", 2],
            ["ex_date__gte=2020-12-01&ex_date__lte=2021-12-12", 3]
        ]

        for q in qstrs:
            print(f'query string = {q[0]}')
            result, r = self.dividend_requests.queryDividend(q[0])
            divs = json.loads(r.text)
            # print(f'{divs=}')
            self.assertEqual(q[1], len(divs))

        result, r = self.dividend_requests.queryDividend('ticker__ticker=MC')
        divs = json.loads(r.text)
        self.assertEqual(2, len(divs))

        result, r = self.dividend_requests.queryDividend('ticker__ticker=MSS')
        divs = json.loads(r.text)
        self.assertEqual(1, len(divs))

        """ 以下は上で実行済みのpostData()と同じ内容
        UniqueTogetherValidator前は問題なくポストされる。

        UniqueTogetherValidato ticker, ex_date, div_val
        """
        result = self.dividend_requests.postData({"ticker": 'mc', "ex_date": '2021-12-01',
                                                  "pay_date": '2021-12-01', "div_val": 0.121, "div_rat": 3.6})
        self.assertEqual(result, None)
        logger.debug('16) 配当関連テスト')


test = ApiTest4Ticker()
# test.test_ticker()
# test.test_ticker1()
# test.test_isThisTickerExist()
# test.test_isThisIdExist()
# test.test_new_postData_getAllData()
# test.test_not_exist()
# test.test_post_patch()
# test.test_delete()
test.test_div()
