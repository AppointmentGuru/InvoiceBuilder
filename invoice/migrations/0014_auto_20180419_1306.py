# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-19 13:06
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0013_invoicesettings_include_booking_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='appointments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100, null=True), db_index=True, default=[], size=None),
        ),
    ]