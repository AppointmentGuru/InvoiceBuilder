# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-31 08:11
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0028_auto_20180717_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('practitioner_id', models.CharField(db_index=True, max_length=128)),
                ('customer_id', models.CharField(db_index=True, max_length=128)),
                ('actor_id', models.CharField(db_index=True, max_length=128)),
                ('auto_created', models.BooleanField(db_index=True, default=False, help_text='Checked if this transactions was automatically created by the system')),
                ('appointments', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100, null=True), blank=True, db_index=True, default=[], null=True, size=None)),
                ('type', models.CharField(blank=True, choices=[('Invoice', 'Invoice'), ('Payment', 'Payment')], db_index=True, max_length=10, null=True)),
                ('currency', models.CharField(blank=True, default='ZAR', max_length=4, null=True)),
                ('amount', models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=10)),
                ('method', models.CharField(choices=[('eft', 'eft'), ('cash', 'cash'), ('snapscan', 'snapscan'), ('credit_card', 'credit_card'), ('write_off', 'write_off'), ('unknown', 'unknown'), ('medicalaid', 'medicalaid'), ('gift', 'gift'), ('voucher', 'voucher')], db_index=True, max_length=128)),
                ('date', models.DateTimeField(db_index=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='payment',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='proofofpayment',
            name='payment',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='integrate_medical_aid',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='template',
            field=models.CharField(blank=True, choices=[('basic', 'basic - A simple invoice template'), ('basic_v2', 'basic_v2 - Version 2 of the simple invoice template')], default='basic', max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AddField(
            model_name='transaction',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.Invoice'),
        ),
        migrations.AddField(
            model_name='proofofpayment',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.Transaction'),
        ),
    ]