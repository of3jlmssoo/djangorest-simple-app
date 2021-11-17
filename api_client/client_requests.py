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

    def __init__(self, DJA_UI, DJA_PW, DJA_URL, headers, app):
        DJA_UI = DJA_UI
        DJA_PW = DJA_PW
        self.DJA_URL = DJA_URL
        self.headers = headers
        self.app = app

        self.session = requests.Session()
        self.session.auth = (DJA_UI, DJA_PW)

        r = self.session.get(DJA_URL + self.app + '/', headers=self.headers)
        if r.text != '[]':
            # print(r.text)
            # jtext = json.loads(r.text)
            # jtext
            print('---------------------------------------')
            print('--- please delete the existing data ---')
            print('---------------------------------------')
            self.delete_all_data()

    def delete_all_data(self):

        r = self.session.get(
            self.DJA_URL + self.app + '/',
            headers=self.headers)
        while r.text != '[]':
            id = json.loads(r.text)[0].pop('id')
            # logger.debug(f'     {r.text} and {id=} will be deleted')
            self.delete_data(id)
            r = self.session.get(
                self.DJA_URL + self.app + '/',
                headers=self.headers)

    def delete_data(self, id):
        # ref_code = 204  # No Content => deleted
        ref_code = http_result.NoContentDeleted.value  # No Content => deleted
        # logger.debug(f'     delete_data called.  {id=}')
        r = self.session.delete(self.DJA_URL + self.app +
                                '/' +
                                str(id) +
                                '/', headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    # def post_data(self, ticker_code, params):
    def post_data(self, params):
        pass
        ref_code = http_result.Created.value  # created
        r = self.session.post(
            self.DJA_URL + self.app + '/',
            data=json.dumps(params),
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def patch_data(self, id, params):
        pass
        ref_code = http_result.Created.value  # created
        r = self.session.patch(
            self.DJA_URL + self.app + '/' + str(id) + '/',
            data=json.dumps(params),
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected
        return result, r

    def get_data(self, ticker_code):
        ref_code = http_result.OK.value
        r = self.session.get(
            self.DJA_URL +
            self.app + 'name/?ticker=' +
            ticker_code,
            headers=self.headers)
        result = expected_result.as_expected if r.status_code == ref_code else expected_result.not_expected

        return result, r
