import json
import os
import subprocess
import sys
from typing import Type

# import django
import requests
from django.contrib.auth.models import User
from django.test import TestCase

from tickers.models import Dividend, Ticker


class TickerTest(TestCase):
    """ Test module for Ticker model """

    def __init__(self, *args, **kwargs):
        print(f'--> TickerTest() __init__()')
        super().__init__(*args, **kwargs)

        self.dja_url = None
        self.username = 'testuser'
        self.password = 'ppaasssswwoorrdd'
        self.user = None
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.headers = {'content-type': 'application/json'}

    def env_check(self):
        try:
            # DJA_UI = os.environ['DJA_UI']
            # DJA_PW = os.environ['DJA_PW']
            self.dja_url = os.environ['DJA_URL']
            print(f'{self.dja_url=}')
        except KeyError as e:
            print(f'環境変数が必要')
            # print(f"export DJA_UI='admin'")
            # print(f"export DJA_PW='amincs8000'")
            print(f"export DJA_URL='http://127.0.0.1:8000/'")
            sys.exit()

    def setUp(self):
        print(f'--> setUp()')
        self.env_check()
        user = User(username=self.username)
        user.set_password(self.password)
        user.save()
        self.user = user

    def test_ticker(self):
        print(f'--> test_ticker()')

        print(f'--> 銘柄登録x1 tickerのみ')
        ref_code = 201
        params = {'ticker': 'mc'}
        print(f'{self.dja_url=}')
        r = self.session.post(
            self.dja_url + 'tickers/',
            data=json.dumps(params),
            headers=self.headers)
        ret_data = json.loads(r.text)
        print(f'{ret_data=}')
        id = ret_data.pop('id')
        ref_ticker = {
            'ticker': 'mc',
            'vol1': 0,
            'vol2': 0,
            'accum': 0,
            'owner': 'admin'}
        ref_data = {'status_code': ref_code, 'ticker': ref_ticker}
        ret_data = {'status_code': r.status_code, 'ticker': ret_data}
        self.assertEqual(ref_data, ret_data)

        # self.assertEqual(self.create_return(data), data)

        # @csrf_exempt
        # def ticker_list(request):
        #     """
        #     List all code snippets, or create a new snippet.
        #     """
        #     if request.method == 'GET':
        #         tickers = Ticker.objects.all()
        #         serializer = TickerSerializer(tickers, many=True)
        #         return JsonResponse(serializer.data, safe=False)

        #     elif request.method == 'POST':
        #         data = JSONParser().parse(request)
        #         serializer = TickerSerializer(data=data)
        #         if serializer.is_valid():
        #             serializer.save()
        #             return JsonResponse(serializer.data, status=201)
        #         return JsonResponse(serializer.errors, status=400)

        # @csrf_exempt
        # def ticker_detail(request, pk):
        #     """
        #     Retrieve, update or delete a code snippet.
        #     """
        #     try:
        #         ticker = Ticker.objects.get(pk=pk)
        #     except Ticker.DoesNotExist:
        #         return HttpResponse(status=404)

        #     if request.method == 'GET':
        #         serializer = TickerSerializer(snippet)
        #         return JsonResponse(serializer.data)

        #     elif request.method == 'PUT':
        #         data = JSONParser().parse(request)
        #         serializer = TickerSerializer(snippet, data=data)
        #         if serializer.is_valid():
        #             serializer.save()
        #             return JsonResponse(serializer.data)
        #         return JsonResponse(serializer.errors, status=400)

        #     elif request.method == 'DELETE':
        #         ticker.delete()
        #         return HttpResponse(status=204)
