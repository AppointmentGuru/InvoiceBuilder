# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-25 21:24
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20170825_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineitem',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='terms',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='amount_paid',
            field=models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customer_id',
            field=models.CharField(db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_amount',
            field=models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='object_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), db_index=True, default=[], size=None),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='practitioner_id',
            field=models.CharField(db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('sent', 'sent'), ('paid', 'paid'), ('unpaid', 'unpaid')], db_index=True, default='new', max_length=10),
        ),
        migrations.DeleteModel(
            name='LineItem',
        ),
    ]