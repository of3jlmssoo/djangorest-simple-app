# Generated by Django 3.2.7 on 2021-11-01 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticker',
            name='highlighted',
        ),
    ]