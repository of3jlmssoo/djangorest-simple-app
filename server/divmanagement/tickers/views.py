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


class DividendFilter(filters.FilterSet):
    # ticker = filters.CharFilter(field_name='ticker__ticker', lookup_expr='iexact')
    # ex_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Dividend
        # fields = ['ticker', 'ex_date']
        fields = ('ticker', 'ex_date')


class DividendList(generics.ListCreateAPIView):
    queryset = Dividend.objects.all()
    serializer_class = DividendSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = DividendFilter
    # filterset_fields = ('ticker', 'ex_date')
    search_fields = ['ticker__ticker', 'ex_date']

    filterset_fields = {
        'ticker__ticker': ['exact'],
        'ex_date': ['gte', 'lte', 'exact', 'gt', 'lt']
    }

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DividendDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dividend.objects.all()
    serializer_class = DividendSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class TickerFilter(filters.FilterSet):
    ticker = filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Ticker
        fields = ['ticker', 'id']


class TickerList(generics.ListCreateAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TickerFilter

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TickerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
