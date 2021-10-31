from rest_framework import serializers
from tickers.models import Ticker, LANGUAGE_CHOICES, STYLE_CHOICES


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
    class Meta:
        model = Ticker
        fields = ['ticker', 'vol1', 'vol2', 'accum']