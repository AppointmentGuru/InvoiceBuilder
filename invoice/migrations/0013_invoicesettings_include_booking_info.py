# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-19 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0012_auto_20180321_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicesettings',
            name='include_booking_info',
            field=models.BooleanField(default=True),
        ),
    ]
