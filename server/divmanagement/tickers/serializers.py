from django.contrib.auth.models import User
from rest_framework import serializers

from tickers.models import LANGUAGE_CHOICES, STYLE_CHOICES, Dividend, Ticker

# class TickerSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     ticker = serializers.CharField(
#         required=True,
#         allow_blank=False,
#         max_length=10)
#     # code = serializers.CharField(style={'base_template': 'textarea.html'})
#     # linenos = serializers.BooleanField(required=False)
#     # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#     vol1 = serializers.IntegerField(min_value=0)
#     vol2 = serializers.IntegerField(min_value=0)
#     accum = serializers.IntegerField(min_value=0)

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Ticker.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.ticker = validated_data.get('title', instance.ticker)
#         instance.vol1 = validated_data.get('title', instance.vol1)
#         instance.vol2 = validated_data.get('title', instance.vol2)
#         instance.accum = validated_data.get('title', instance.accum)
#         # instance.code = validated_data.get('code', instance.code)
#         # instance.linenos = validated_data.get('linenos', instance.linenos)
#         # instance.language = validated_data.get('language', instance.language)
#         # instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance


class TickerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    # dividend_set = DividendSerializer(many=True)

    class Meta:
        model = Ticker
        fields = ['ticker', 'vol1', 'vol2', 'accum', 'owner']

    # def create(self, validated_data):
    #     dividend_validated_data = validated_data.pop('dividend_set')
    #     question = Question.objects.create(**validated_data)
    #     dividend_set_serializer = self.fields['dividend_set']
    #     for each in dividend_validated_data:
    #         each['ticker'] = ticker
    #     dividends = dividend_set_serializer.create(dividend_validated_data)
    #     return question


class DividendSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # ticker = TickerSerializer()
    # ticker = serializers.StringRelatedField()
    # ticker = serializers.CharField(source='ticker.ticker')
    # print(f'{ticker=}')

    class Meta:
        model = Dividend
        fields = [
            'ticker',
            'ex_date',
            'pay_date',
            'div_val',
            'div_rat',
            'owner']

        # def craete(self, data):
        #     ticker, __ = Ticker.objects.get_or_create(ticke=data['ticker'])
        #     return Dividend()
    # def create(self, validated_data):
    #     return Dividend.objects.create(**validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        print(f'==> to_representation {rep=} {type(rep)=}')
        print(f'==> to_representation {Ticker(instance.ticker).ticker=}')
        # rep['ticker'] = Ticker(instance.ticker).ticker
        return rep

    # def to_representation(self, instance):
    #     rep = super(DividendSerializer, self).to_representation(instance)
    #     print(f'{instance.ticker.ticker=}')
    #     rep['ticker'] = instance.ticker.ticker
    #     return rep

    # def to_representation(self, instance):
    #     rep = super(UserSerializer, self).to_representation(instance)
    #     rep['company_name'] = instance.company_name.name
    #     return rep

    # preparation for create()
    # def create(self, data):
    #     print(f'==> {data["ticker"]=} {type(data["ticker"])=}')
    #     tk1, tk2 = Ticker.objects.get_or_create(ticker=data["ticker"])
    #     print(f'==> {tk1=} {type(tk1)=} {tk2=}')
    #     dividend = Dividend(
    #         ticker=tk1,
    #         ex_date=data['ex_date'],
    #         pay_date=data['pay_date'],
    #         div_val=data['div_val'],
    #         div_rat=data['div_rat'],
    #         owner=data['owner']
    #     )
    #     dividend.save()
    #     print(f'{dividend=} {tk1=} ')
    #     return dividend


class UserSerializer(serializers.ModelSerializer):
    tickers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ticker.objects.all())

    class Meta:
        model = User
        fields = ['ticker', 'vol1', 'vol2', 'accum']
