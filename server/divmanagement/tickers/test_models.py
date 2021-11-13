from django.contrib.auth.models import User
from django.test import TestCase
import django
from tickers.models import Dividend, Ticker


class TickerTest(TestCase):
    """ Test module for Ticker model """

    def __init__(self, *args, **kwargs):
        print(f'--> TickerTest')
        super().__init__(*args, **kwargs)
        self.user = ''

    def setUp(self):
        print(f'--> setUp called')
        user = User(username='testusr')
        user.set_password('ppaasssswwoorrdd')
        user.save()
        # data0 = {
        #     'ticker': 'mc',
        #     'vol1': 3,
        #     'vol2': 2,
        #     'accum': 50,
        #     'owner': 'user'}
        self.user = user
        # Ticker.objects.create(
        #     ticker=self.data0['ticker'],
        #     vol1=self.data0['vol1'],
        #     vol2=self.data0['vol2'],
        #     accum=self.data0['accum'],
        #     owner=self.data0['owner'])

        # Ticker.objects.create(
        #     ticker='mc',
        #     vol1=3,
        #     vol2=2,
        #     accum=50,
        #     owner=user)
        # Ticker.objects.create(
        #     ticker='mss', vol1=5, vol2=3, accum=70, owner='user1')

    def test_ticker(self):
        print(f'--> Ticker_breed called')
        # Ticker_mc = Ticker.objects.get(ticker='mc')
        # Ticker_mss = Ticker.objects.get(ticker='mss')
        # dataR = {
        #     'ticker': Ticker_mc.ticker,
        #     'vol1': Ticker_mc.vol1,
        #     'vol2': Ticker_mc.vol2,
        #     'accum': Ticker_mc.accum,
        #     'owner': Ticker_mc.owner}

        # print(f'{type(self.data0)=}')
        # print(f'{type(dataR)=}')
        # print(f'{Ticker_mc=}')
        # print(f'{type(Ticker_mc)=}')
        # print(f'{Ticker_mc.ticker=}')
        # print(f'{Ticker_mc.vol1=}')
        data = {
            'ticker': 'mc',
            'vol1': 3,
            'vol2': 2,
            'accum': 50,
            'owner': self.user}
        self.assertEqual(self.create_return(data), data)

        data = {
            'ticker': None,
            'vol1': 3,
            'vol2': 2,
            'accum': 50,
            'owner': self.user}
        # self.assertEqual(self.create_return(data), data)

        self.assertRaises(
            django.db.utils.IntegrityError,
            self.create_return,
            data)

        # self.assertEqual(
        #     Ticker_muffin.get_breed(), "Muffin belongs to Gradane breed.")

    def create_return(self, data):
        # print(f'--> create_return() {data=}')
        Ticker_mc = Ticker.objects.create(
            ticker=data['ticker'],
            vol1=data['vol1'],
            vol2=data['vol2'],
            accum=data['accum'],
            owner=data['owner'])

        print(f'--> create_return() {Ticker_mc=} {Ticker_mc.ticker=}')
        if Ticker_mc:
            print(f'--> True')
        else:
            print(f'--> Else')

        return {
            'ticker': Ticker_mc.ticker,
            'vol1': Ticker_mc.vol1,
            'vol2': Ticker_mc.vol2,
            'accum': Ticker_mc.accum,
            'owner': Ticker_mc.owner}

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
