# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-13 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20170828_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_period_from',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='invoice_period_to',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='template',
            field=models.CharField(blank=True, choices=[('basic', 'basic - A simple invoice template')], default='basic', max_length=255, null=True),
        ),
    ]
