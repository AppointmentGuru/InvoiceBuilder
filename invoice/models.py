from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils import timezone
import uuid, requests

from .helpers import (
    fetch_data,
    fetch_appointments,
    to_context,
    clean_context
)

INVOICE_STATUSES = [
    ('new', 'new'),
    ('sent', 'sent'),
    ('paid', 'paid'),
    ('unpaid', 'unpaid'),
]

TEMPLATES = [(key, '{} - {}'.format(key, values.get('title'))) for key, values in settings.TEMPLATE_REGISTRY.items()]

def get_uuid():
  return str(uuid.uuid4())

def get_short_uuid():
    return str(uuid.uuid4()).split('-')[0]

"""
class InvoiceSettings(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name =  models.CharField(max_length=255, blank=True, null=True)

    # configs:
    template = models.CharField(max_length=255, blank=True, null=True, help_text='The base template to use for invoices using these settings')
"""

class InvoiceSettings(models.Model):
    '''
    Global settings that apply to all generated invoices
    '''

    practitioner_id = models.CharField(max_length=128, db_index=True)
    quote_notes = models.TextField(blank=True, null=True)
    invoice_notes = models.TextField(blank=True, null=True)
    receipt_notes = models.TextField(blank=True, null=True)

    invoice_address = models.TextField(blank=True, null=True, help_text='Your address as shown on invoices' )
    customer_info = models.TextField(blank=True, null=True, help_text='Choose how you would like to display your customers info')
    lineitem_template = models.TextField(blank=True, null=True, default='codetable.html')


class Invoice(models.Model):

    def __str__(self):
        return '#{}: {}'.format(self.invoice_number, self.title)

    # relationships
    practitioner_id = models.CharField(max_length=128, db_index=True)
    customer_id = models.CharField(max_length=128, db_index=True)
    appointments = ArrayField(models.CharField(max_length=100), default=[], db_index=True)

    object_ids = ArrayField(models.CharField(max_length=100), default=[], db_index=True)

    sender_email = models.EmailField(default='support@appointmentguru.co')
    # invoice_number = models.CharField(max_length=255,blank=True, null=True)
    title = models.CharField(max_length=255,blank=True, null=True)
    status = models.CharField(max_length=10, choices=INVOICE_STATUSES, default='new', db_index=True)

    context = JSONField(default={})
    template = models.CharField(max_length=255, blank=True, null=True, choices=TEMPLATES, default='basic')

    password = models.CharField(max_length=255, blank=True, null=True, default=get_short_uuid)
    customer_password = models.CharField(max_length=255, blank=True, null=True, default=get_short_uuid)

    currency = models.CharField(max_length=4,blank=True, null=True, default='ZAR')
    invoice_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0, db_index=True)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10, default=0, db_index=True)

    date = models.DateField(default=timezone.now, db_index=True, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True, db_index=True)

    invoice_period_from = models.DateField(db_index=True, blank=True, null=True)
    invoice_period_to = models.DateField(db_index=True, blank=True, null=True)

    short_url = models.URLField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    def get_short_url(self, force=False, admin_url=True):
        '''
        curl https://www.googleapis.com/urlshortener/v1/url?key=... \
            -H 'Content-Type: application/json' \
            -d '{"longUrl": "https://google.com"}'
        '''
        url = 'https://www.googleapis.com/urlshortener/v1/url'
        params = {
            "key": settings.GOOGLE_API_SHORTENER_TOKEN
        }

        if admin_url:
            url_to_shorten = self.admin_invoice_url
        else:
            url_to_shorten = self.customer_invoice_url

        result = requests.post(
            url,
            json={'longUrl': url_to_shorten},
            params=params)
        short_url = result.json().get('id')
        self.short_url = short_url
        self.save()
        return short_url

    def get_context(self, default_context = {}):

        practitioner, appointments, medical_record = fetch_data(
            self.practitioner_id,
            self.appointment_ids,
            self.customer_id)

        context = to_context(
                    practitioner,
                    appointments,
                    medical_record,
                    default_context=default_context,
                    format_times = False,
                    format_codes = False)
        context = clean_context(context)
        self.context = context
        return context

    def apply_settings(self):
        '''
        Apply invoice settings to invoice
        '''
        pass


    @property
    def invoice_number(self):
        if self.title is None: return 'INV-{}'.format(self.id)
        initials = ("").join([word[0:1].upper() for word in self.title.split(' ') if word.isalpha()])
        return '{}-{}'.format(initials, self.id)

    @property
    def admin_invoice_url(self):
        base = settings.INVOICEGURU_BASE_URL
        return '{}/invoice/{}?key={}'.format(base, self.pk, self.password)

    @property
    def customer_invoice_url(self):
        base = settings.INVOICEGURU_BASE_URL
        return '{}/invoice/{}?key={}'.format(base, self.pk, self.customer_password)

from .signals import *