from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Ticker(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ticker = models.CharField(max_length=10, blank=False, null=False)
    vol1 = models.IntegerField(validators=[MinValueValidator(0)])
    vol2 = models.IntegerField(validators=[MinValueValidator(0)])
    accum = models.IntegerField(validators=[MinValueValidator(0)])
    # code = models.TextField()
    # linenos = models.BooleanField(default=False)
    # language = models.CharField(
    #     choices=LANGUAGE_CHOICES,
    #     default='python',
    #     max_length=100)
    # style = models.CharField(
    #     choices=STYLE_CHOICES,
    #     default='friendly',
    #     max_length=100)

    class Meta:
        ordering = ['created']
