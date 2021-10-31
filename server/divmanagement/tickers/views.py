from rest_framework import generics

from tickers.models import Ticker
from tickers.serializers import TickerSerializer


class TickerList(generics.ListCreateAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer


class TickerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer


# from django.http import Http404, HttpResponse, JsonResponse
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
# from rest_framework.response import Response
# from rest_framework.views import APIView

# #     elif request.method == 'DELETE':
# #         ticker.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
# from tickers.models import Ticker
# from tickers.serializers import TickerSerializer

# # # Create your views here.


# # # @csrf_exempt
# # # def ticker_list(request):
# # #     """
# # #     List all code tickers, or create a new Ticker.
# # #     """
# # #     if request.method == 'GET':
# # #         tickers = Ticker.objects.all()
# # #         serializer = TickerSerializer(tickers, many=True)
# # #         return JsonResponse(serializer.data, safe=False)

# # #     elif request.method == 'POST':
# # #         data = JSONParser().parse(request)
# # #         serializer = TickerSerializer(data=data)
# # #         if serializer.is_valid():
# # #             serializer.save()
# # #             return JsonResponse(serializer.data, status=201)
# # #         return JsonResponse(serializer.errors, status=400)


# # # @csrf_exempt
# # # def ticker_detail(request, pk):
# # #     """
# # #     Retrieve, update or delete a code Ticker.
# # #     """
# # #     try:
# # #         ticker = Ticker.objects.get(pk=pk)
# # #     except Ticker.DoesNotExist:
# # #         return HttpResponse(status=404)

# # #     if request.method == 'GET':
# # #         serializer = TickerSerializer(Ticker)
# # #         return JsonResponse(serializer.data)

# # #     elif request.method == 'PUT':
# # #         data = JSONParser().parse(request)
# # #         serializer = TickerSerializer(Ticker, data=data)
# # #         if serializer.is_valid():
# # #             serializer.save()
# # #             return JsonResponse(serializer.data)
# # #         return JsonResponse(serializer.errors, status=400)

# # #     elif request.method == 'DELETE':
# # #         ticker.delete()
# # #         return HttpResponse(status=204)


# # @api_view(['GET', 'POST'])
# # def ticker_list(request, format=None):
# #     """
# #     List all code tickers, or create a new Ticker.
# #     """
# #     if request.method == 'GET':
# #         tickers = Ticker.objects.all()
# #         serializer = TickerSerializer(tickers, many=True)
# #         return Response(serializer.data)

# #     elif request.method == 'POST':
# #         serializer = TickerSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # @api_view(['GET', 'PUT', 'DELETE'])
# # def ticker_detail(request, pk, format=None):
# #     """
# #     Retrieve, update or delete a code Ticker.
# #     """
# #     try:
# #         ticker = Ticker.objects.get(pk=pk)
# #     except Ticker.DoesNotExist:
# #         return Response(status=status.HTTP_404_NOT_FOUND)

# #     if request.method == 'GET':
# #         serializer = TickerSerializer(ticker)
# #         return Response(serializer.data)

# #     elif request.method == 'PUT':
# #         serializer = TickerSerializer(ticker, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TickerList(APIView):
#     """
#     List all tickers, or create a new Ticker.
#     """

#     def get(self, request, format=None):
#         tickers = Ticker.objects.all()
#         serializer = TickerSerializer(tickers, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = TickerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TickerDetail(APIView):
#     """
#     Retrieve, update or delete a Ticker instance.
#     """

#     def get_object(self, pk):
#         try:
#             return Ticker.objects.get(pk=pk)
#         except Ticker.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         Ticker = self.get_object(pk)
#         serializer = TickerSerializer(Ticker)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         Ticker = self.get_object(pk)
#         serializer = TickerSerializer(Ticker, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         Ticker = self.get_object(pk)
#         Ticker.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
