from django.test import TestCase

# # Create your tests here.
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from tickers.models import Ticker
# from tickers.serializers import TickerSerializer


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
