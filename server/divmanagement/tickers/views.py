from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters, generics, permissions
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from tickers.models import Dividend, Ticker
from tickers.permissions import IsOwnerOrReadOnly
from tickers.serializers import (DividendSerializer, TickerSerializer,
                                 UserSerializer)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'tickers': reverse('ticker-list', request=request, format=format)
    })


class DividendList(generics.ListCreateAPIView):
    queryset = Dividend.objects.all()
    serializer_class = DividendSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DividendDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dividend.objects.all()
    serializer_class = DividendSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

# 3


class TickerList(generics.ListCreateAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TickerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class TickerFilter(filters.FilterSet):
    # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    # ticker = django_filters.CharFilter(lookup_expr='iexact')
    ticker = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Ticker
        fields = ['ticker']


class TickerListAPIView(generics.ListAPIView):
    print(f'=== TickerListAPIView called ===')
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TickerFilter
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
