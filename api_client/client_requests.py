"""
export DJA_UI='admin'
export DJA_PW='amincs8000'
export DJA_URL='http://127.0.0.1:8000/'

200 OK
201 Created
204 No Content => deleted
400 Bad Request

2つ確認するものがある。
1. HTTPレベル
2. アプリレベル

get_data_of_ticket  : HTTPレベルのステータスコードをチェック
isThisTickerExist   : if HTTP = Good & アプリレベル = Good
                        return 0
                      else
                        return r

"""
import json
import logging
from typing import Union

import requests

from resultenum import expected_result, http_result

# from django.test import TestCase


# import os
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


class client_requests(object):

    def __init__(self, DJA_UI, DJA_PW, DJA_URL, headers, app):
        # def __init__(self, DJA_UI, DJA_PW, DJA_URL, headers):
        DJA_UI = DJA_UI
        DJA_PW = DJA_PW
        self.DJA_URL = DJA_URL
        self.headers = headers
        self.app = app

        self.session = requests.Session()
        self.session.auth = (DJA_UI, DJA_PW)

        # r = self.session.get(DJA_URL + self.app + '/', headers=self.headers)
        # if r.text != '[]':
        #     # print(r.text)
        #     # jtext = json.loads(r.text)
        #     # jtext
        #     print('---------------------------------------')
        #     print('--- please delete the existing data ---')
        #     print('---------------------------------------')
        #     self.delete_all_data()

    def delete_all_data(self):

        r = self.session.get(
            # self.DJA_URL + self.app + '/',
            self.DJA_URL + self.app + '/',
            headers=self.headers)
        while r.text != '[]':
            id = json.loads(r.text)[0].pop('id')
            self.delete_data(id)
            r = self.session.get(
                # self.DJA_URL + self.app + '/',
                self.DJA_URL + self.app + '/',
                headers=self.headers)

    def delete_data(self, id):
        ref_code = http_result.NoContentDeleted.value  # No Content => deleted
        r = self.session.delete(self.DJA_URL + self.app +
                                '/' +
                                str(id) +
                                '/', headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def post_data(self, params):
        pass
        ref_code = http_result.Created.value  # created
        r = self.session.post(
            self.DJA_URL + self.app + '/',
            data=json.dumps(params),
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def postData(self, params) -> Union[str, None]:
        result, r = self.post_data(params)
        """ TODO : エラーチェック強化検討。辞書のキー毎に正しいか確認するかどうか """
        if result == expected_result.as_expected and r.text != '[]':
            return json.loads(r.text)
        else:
            return None

    def patch_data(self, id, params):
        pass
        # ref_code = http_result.Created.value  # created
        ref_code = http_result.OK.value  # created
        r = self.session.patch(
            self.DJA_URL + self.app + '/' + str(id) + '/',
            data=json.dumps(params),
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def patchData(self, id, params) -> Union[dict, None]:
        pass
        result, r = self.patch_data(id, params)
        if result != expected_result.as_expected:
            print(f'client_request.patchData() failed. {id=} {params=}')
            return None
        print(f'==> {r.status_code=}')
        patched_ticker = json.loads(r.text)
        for k in params.keys():
            if params[k] != patched_ticker[k]:
                return None
        return patched_ticker

    def get_data_of_ticker(self, ticker_code):
        ref_code = http_result.OK.value
        r = self.session.get(
            self.DJA_URL +
            self.app + '/?ticker=' +
            ticker_code,
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def getIdOfTicker(self, ticker_code) -> Union[int, None]:
        if (result := self.isThisTickerExist(ticker_code)):
            return result["id"]
        return None

    def isThisTickerExist(self, ticker_code) -> Union[str, None]:
        result, r = self.get_data_of_ticker(ticker_code)
        # print(f'{r.__sizeof__()}')
        # print(f'{type(r.text)=}')
        # print(f'{r.json()=}')
        # print(f'{r.content=}')
        if result == expected_result.as_expected and r.text != '[]':
            # data = json.loads(r.text)[0]
            # print(f'==> {type(data)=}')
            return json.loads(r.text)[0]
        else:
            return None

    def getAllData(self) -> Union[str, None]:
        result, r = self.get_data_of_all()
        if result == expected_result.as_expected and r.text != '[]':
            # return r.text
            return json.loads(r.text)
        else:
            return None

    def get_data_of_all(self):
        ref_code = http_result.OK.value
        r = self.session.get(
            self.DJA_URL +
            self.app + '/',
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def pop_id_from_POST_data(self, rtext):
        ret_ticker = json.loads(rtext)
        id = ret_ticker.pop('id')
        return id, ret_ticker

    def pop_id_from_GET_data(self, rtext):
        """
        def get_data_of_ticker ()はticker_codeを指定している。モデルでTickerのtickerはunique=Trueなので複数返されることはない
        """
        ret_ticker = json.loads(rtext)[0]
        id = ret_ticker.pop('id')
        return id, ret_ticker


# class ticker_requests(client_requests):

#     def __init__(self, DJA_UI, DJA_PW, DJA_URL, headers, app):

#         super().__init__(DJA_UI, DJA_PW, DJA_URL, headers, app)

#     def pop_id_from_POST_data(self, rtext):
#         ret_ticker = json.loads(rtext)
#         id = ret_ticker.pop('id')
#         return id, ret_ticker

#     def pop_id_from_GET_data(self, rtext):
#         """
#         def get_data_of_ticker ()はticker_codeを指定している。モデルでTickerのtickerはunique=Trueなので複数返されることはない
#         """
#         ret_ticker = json.loads(rtext)[0]
#         id = ret_ticker.pop('id')
#         return id, ret_ticker


# class dividend_requests(client_requests):

#     def __init__(self, DJA_UI, DJA_PW, DJA_URL, headers, app):

#         super().__init__(DJA_UI, DJA_PW, DJA_URL, headers, app)

#     def pop_id_from_POST_data(self, rtext):
#         ret_ticker = json.loads(rtext)
#         id = ret_ticker.pop('id')
#         return id, ret_ticker

#     def pop_id_from_GET_data(self, rtext):
#         """
#         def get_data_of_ticker ()はticker_codeを指定している。モデルでTickerのtickerはunique=Trueなので複数返されることはない
#         """
#         ret_ticker = json.loads(rtext)[0]
#         id = ret_ticker.pop('id')
#         return id, ret_ticker
