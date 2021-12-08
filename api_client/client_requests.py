"""
200 OK
201 Created
204 No Content => deleted
400 Bad Request

2つ確認するものがある。
1. HTTPレベル
2. アプリレベル

メソッド説明
delete_data()   :   Python requestsを使っているメソッド。deleteコマンドをコールしているだけ
deleteData()    :   外部からはこちらを呼び出す。
                    delete_data()を呼び出す。
                    delete_data()を呼び出す前にidのチェック、isThisTickerExistなどを行っている


メソッド一覧
外部から呼出を想定したメソッド      内部使用のメソッド
deleteAllData()                     delete_all_data()
deleteData()                        delete_data()
postData()                          post_data()
patchData()                         patch_data()
getDataOfTicker(),getDataOfId()     get_data_of()
getIdOfTicker()
queryDividend()
isThisTickerExist()
getAllData()                        get_data_of_all()
pop_id_from_POST_data()
pop_id_from_GET_data()

"""
import json
import logging
from typing import Tuple, Union

import requests
from requests.models import Response

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


class client_requests(object):

    def __init__(self, DJA_UI, DJA_PW, DJA_URL, headers, app) -> None:
        DJA_UI = DJA_UI
        DJA_PW = DJA_PW
        self.DJA_URL = DJA_URL
        self.headers = headers
        self.app = app

        self.session = requests.Session()
        self.session.auth = (DJA_UI, DJA_PW)

    def delete_all_data(self) -> None:
        """ objects.all.delete()を利用するでもいけそうではある """

        r = self.session.get(
            self.DJA_URL + self.app + '/',
            headers=self.headers)

        data = json.loads(r.text)

        for t in data:
            self.delete_data(t["id"])

    def deleteAllData(self) -> None:
        self.delete_all_data()

    def delete_data(self, id: int) -> Tuple[expected_result, Response]:
        # def delete_data(self, id: int):
        ref_code = http_result.NoContentDeleted.value  # No Content => deleted
        r = self.session.delete(self.DJA_URL + self.app +
                                '/' +
                                str(id) +
                                '/', headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def deleteData(self, id: int) -> bool:
        """ type(id)がintであることをチェック """
        if not isinstance(id, int):
            print(f'client_requests.deleteData invalid arg {id=}')
            return False

        """ idが存在することをチェック """
        result = self.isThisTickerExist(id)
        if not result:
            print(f'client_requests.deleteData ticker doesnot exist {id}')
            return False

        """ delete_data(id)"""
        result, r = self.delete_data(id)
        if result:
            return True

        print('client_requests.deleteData delete_data called but error occurred.')
        return False

    def post_data(self, params: dict) -> Tuple[expected_result, Response]:

        ref_code = http_result.Created.value  # created
        r = self.session.post(
            self.DJA_URL + self.app + '/',
            data=json.dumps(params),
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def postData(self, params: dict) -> Union[str, None]:
        """ TODO: paramsのキー、値の型チェック、数値の場合の条件(+ only等)を追加する余地あり """
        if not isinstance(params, dict):
            print(f'client_request.postData not instance of dict:{params=}')
            return None

        """ 必須キー(tickerの場合ticker)の指定有無確認 """
        for reqkey in ['ticker']:  # , 'ex_date', 'div_val']:  # , 'owner']:
            if reqkey not in params.keys():
                print(f'client_request.postData key missing:{reqkey}')
                return None

        # if params['ticker'] == 'NTR':
        #     print(f'============={params["ticker"]}====================')
        #     params['ticker'] = 'ntr'
        """ tickerは大文字に揃える """
        params['ticker'] = params['ticker'].upper()

        result, r = self.post_data(params)
        """ TODO : エラーチェック強化検討。辞書のキー毎に正しいか確認するかどうか """
        if result == expected_result.as_expected and r.text != '[]':
            return json.loads(r.text)
        else:
            return None

    def patch_data(self, id: int, params: dict) -> Tuple[expected_result, Response]:
        """ paramsに存在しないキーを指定した場合、r.status_code == 200 Okで処理されてしまう"""
        pass

        # print(f'patch_data {params=}')
        ref_code = http_result.OK.value  # created
        r = self.session.patch(
            self.DJA_URL + self.app + '/' + str(id) + '/',
            data=json.dumps(params),
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected

        # print(f'patch_data {r.status_code=}')
        return result, r

    def patchData(self, id: int, params: dict) -> Union[dict, None]:
        """ paramsのキー、値の型チェック、数値の場合の条件(+ only等)を追加する余地あり """

        """ tickerは大文字に揃える """
        if 'ticker' in params.keys():
            params['ticker'] = params['ticker'].upper()

        result = self.isThisTickerExist(id)
        if not result:
            print(f'client_requests.patchData ticker doesnot exist {id}')
            return None

        if not isinstance(id, int) or not isinstance(params, dict):
            print(f'client_requests.patchData error {type(id)} {type(params)}')
            return None

        valid_keys = result.keys()
        for k in params.keys():
            if k not in valid_keys:
                print(f'client_requests.patchData invalid key specified {k}')
                return None

        result, r = self.patch_data(id, params)
        if result != expected_result.as_expected:
            print(
                f'client_request.patchData failed. {result=} {r.status_code=} {id=} {params=}')
            print(f'client_request.patchData {self.getAllData()=}')
            return None
        patched_ticker = json.loads(r.text)
        # print(f'patchData {self.getAllData()=}')
        for k in params.keys():
            # if int(params[k]) != patched_ticker[k]:
            if params[k] != patched_ticker[k]:
                print(f'{k=} {params[k]=} {patched_ticker[k]}')
                return None
        return patched_ticker

    def get_data_of(self, key: str, identifier: str) -> Tuple[expected_result, Response]:
        ref_code = http_result.OK.value
        r = self.session.get(
            self.DJA_URL +
            self.app + '/?' + key + '=' +
            identifier,
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def getDataOfTicker(self, ticker_information: str) -> Tuple[expected_result, Response]:
        if not isinstance(ticker_information, str):
            print(
                f'client_request.getDataOfTicker error:{type(ticker_information)=} not str')
        return self.get_data_of('ticker', ticker_information.upper())

    def getDataOfId(self, ticker_information: int) -> Tuple[expected_result, Response]:
        return self.get_data_of('id', str(ticker_information))

    def getIdOfTicker(self, ticker_code: str) -> Union[int, None]:
        if not isinstance(ticker_code, str):
            print(
                f'client_request.getIdOfTicker error: {type(ticker_code)=} not str')
            return None
        if (result := self.isThisTickerExist(ticker_code.upper())):
            return result["id"]
        return None

    def queryDividend(self, query_str: str) -> Tuple[expected_result, Response]:
        pass
        ref_code = http_result.OK.value
        r = self.session.get(
            self.DJA_URL +
            self.app + '/?' + query_str,
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def isThisTickerExist(self, ticker_information: Union[str, int]) -> Union[dict, None]:
        if not isinstance(
                ticker_information,
                str) and not isinstance(
                ticker_information,
                int):
            print(
                f'client_request.isThisTickerExist error: {type(ticker_information)=} not str and int')
            return None

        if isinstance(ticker_information, str):
            result, r = self.getDataOfTicker(ticker_information.upper())
        if isinstance(ticker_information, int):
            result, r = self.getDataOfId(ticker_information)

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

    def get_data_of_all(self) -> Tuple[expected_result, Response]:
        ref_code = http_result.OK.value
        r = self.session.get(
            self.DJA_URL +
            self.app + '/',
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def pop_id_from_POST_data(self, rtext: str) -> Tuple[int, dict]:
        ret_ticker = json.loads(rtext)
        id = ret_ticker.pop('id')
        return id, ret_ticker

    def pop_id_from_GET_data(self, rtext: str) -> Tuple[int, dict]:
        """
        def getDataOfTicker ()はticker_codeを指定している。モデルでTickerのtickerはunique=Trueなので複数返されることはない
        """
        ret_ticker = json.loads(rtext)[0]
        id = ret_ticker.pop('id')
        return id, ret_ticker
