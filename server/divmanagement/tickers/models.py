from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Ticker(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ticker = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        unique=True,
    )
    # default='someerror')
    vol1 = models.IntegerField(
        validators=[
            MinValueValidator(0)],
        blank=False,
        null=False,
        default=0
    )
    vol2 = models.IntegerField(validators=[MinValueValidator(0)],
                               blank=False,
                               null=False,
                               default=0)
    total_vol = models.IntegerField(validators=[MinValueValidator(0)],
                                    blank=False,
                                    null=False,
                                    default=0)
    accum = models.IntegerField(validators=[MinValueValidator(0)],
                                blank=False,
                                null=False,
                                default=0)

    owner = models.ForeignKey(
        'auth.User',
        related_name='tickers',
        on_delete=models.CASCADE)
    # highlighted = models.TextField()

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

    def save(self, *args, **kwargs):
        # """
        # Use the `pygments` library to create a highlighted HTML
        # representation of the code snippet.
        # """
        # lexer = get_lexer_by_name('Markdown')
        # # linenos = 'table' if self.linenos else False
        # # options = {'title': self.title} if self.title else {}
        # formatter = HtmlFormatter(full=True)
        # self.highlighted = highlight(self.ticker, lexer, formatter)
        self.total_vol = self.vol1 + self.vol2
        super(Ticker, self).save(*args, **kwargs)

    def __str__(self):
        return self.ticker


"""
確定日 : ex_date : 日付
支払日 : pay_date : 日付
配当額 : div_val : float
配当率 : div_rat : float
"""


class Dividend(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    ticker = models.ForeignKey(
        Ticker,
        to_field='ticker',
        on_delete=models.PROTECT)
    ex_date = models.DateField(blank=False, null=False)
    pay_date = models.DateField(blank=True, null=True, default='2020/1/1')
    div_val = models.DecimalField(
        max_digits=8,
        decimal_places=6,
        blank=False,
        null=False)
    div_rat = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True, default=0.0)

    owner = models.ForeignKey(
        'auth.User',
        related_name='dividends',
        on_delete=models.CASCADE)
    # highlighted = models.TextField()

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

    def save(self, *args, **kwargs):
        super(Dividend, self).save(*args, **kwargs)


"""
div_val
max_digits 12.123456 => 8
decimal_places => 6

div_rat
max_digits 12.12=> 4
decimal_places => 2

"""
