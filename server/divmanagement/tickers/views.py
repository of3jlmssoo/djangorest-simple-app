from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from tickers.models import Ticker
from tickers.serializers import TickerSerializer

# Create your views here.


# @csrf_exempt
# def ticker_list(request):
#     """
#     List all code tickers, or create a new snippet.
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


@api_view(['GET', 'POST'])
def ticker_list(request, format=None):
    """
    List all code tickers, or create a new snippet.
    """
    if request.method == 'GET':
        tickers = Ticker.objects.all()
        serializer = TickerSerializer(tickers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TickerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ticker_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        ticker = Ticker.objects.get(pk=pk)
    except Ticker.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TickerSerializer(ticker)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TickerSerializer(ticker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ticker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
