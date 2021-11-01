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
        unique=True)
    vol1 = models.IntegerField(validators=[MinValueValidator(0)])
    vol2 = models.IntegerField(validators=[MinValueValidator(0)])
    total_vol = models.IntegerField(validators=[MinValueValidator(0)])
    accum = models.IntegerField(validators=[MinValueValidator(0)])

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
