from django.contrib.auth.models import User
from rest_framework import serializers

from tickers.models import LANGUAGE_CHOICES, STYLE_CHOICES, Dividend, Ticker


class TickerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ticker
        fields = ['id', 'ticker', 'vol1', 'vol2', 'accum', 'owner']


class DividendSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dividend
        fields = [
            'ticker',
            'ex_date',
            'pay_date',
            'div_val',
            'div_rat',
            'owner']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        print(f'==> to_representation {rep=} {type(rep)=}')
        print(f'==> to_representation {Ticker(instance.ticker).ticker=}')
        return rep


class UserSerializer(serializers.ModelSerializer):
    tickers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ticker.objects.all())

    class Meta:
        model = User
        fields = ['ticker', 'vol1', 'vol2', 'accum']
