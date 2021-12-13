from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from tickers.models import LANGUAGE_CHOICES, STYLE_CHOICES, Dividend, Ticker


class TickerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Ticker
        fields = [
            'id',
            'ticker',
            'vol1',
            'vol2',
            # 'total_vol',
            'accum',
            'owner']


class DividendSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dividend
        fields = [
            'id',
            'ticker',
            'ex_date',
            'pay_date',
            'div_val',
            'div_rat',
            'owner']
        validators = [
            # r.text = '{"non_field_errors":["DividendSerializer the dividend already registered"]}'
            UniqueTogetherValidator(
                queryset=Dividend.objects.all(),
                fields=['ticker', 'ex_date', 'div_val'],
                message='DividendSerializer the dividend already registered'
            )
        ]

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
