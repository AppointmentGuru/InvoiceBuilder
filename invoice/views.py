'''
Views for displaying invoices
'''
from dateutil.parser import parse
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from decimal import Decimal
from dateutil import parser
from .helpers import fetch_data, to_context, codes_to_table
from .models import Invoice


@user_passes_test(lambda u: u.is_superuser)
def invoices(request, practitioner, from_date, to_date):
    '''
    '''
    parsed_from = parser.parse(from_date)
    parsed_to = parser.parse(to_date)
    invoices = Invoice.objects.filter(
        practitioner_id=practitioner,
        date__gte=parsed_from,
        date__lte=parsed_to)

    total_value = sum([invoice.invoice_amount for invoice in invoices])
    context = {
        'invoices': invoices,
        'parsed_from': parsed_from,
        'parsed_to': parsed_to,
        'total_value': total_value,
    }
    return render(request, 'invoice/list.html', context=context)

@csrf_exempt
def invoice(request, pk):
    password = request.GET.get('key')
    invoice = get_object_or_404(Invoice, pk=pk, password=password)

    template_key = request.GET.get('template', invoice.template)
    template_data = settings.TEMPLATE_REGISTRY.get(template_key)
    template_path = 'invoice/templates/{}'.format(template_data.get('filename', 'basic.html'))

    context = invoice.context
    invoice_total = 0
    for appt in context.get('appointments', []):
        appt['start_time_formatted'] = parse(appt.get('start_time'))
        codes = appt.get('codes', None)
        if codes is not None and len(codes) > 0:
            appt['codes_formatted'] = codes_to_table(codes)
        invoice_total += Decimal(appt.get('price', 0))

    context['invoice'] = invoice
    context['amount_due'] = Decimal(invoice.invoice_amount) - Decimal(invoice.amount_paid)
    return render(request, template_path, context=context)

@csrf_exempt
def preview(request):
    practitioner_id = request.GET.get('practitioner_id')
    appointment_ids = request.GET.get('appointment_ids', '').split(',')
    client_id = request.GET.get('client_id')

    practitioner, appointments, medical_record = fetch_data(practitioner_id, appointment_ids, client_id)
    context = to_context(practitioner, appointments, medical_record)
    return render(request, 'invoice/templates/basic.html', context=context)

# docker run -v $(pwd):/downloads/ aquavitae/weasyprint weasyprint http://weasyprint.org /downloads/invoice.pdf

# import docker, os
# client = docker.from_env()
# volumes = { os.getcwd(): { 'bind': '/downloads/' } }
# client.containers.run("aquavitae/weasyprint", "weasyprint http://weasyprint.org /downloads/invoice.pdf", volumes=volumes)

# client.containers.run('alpine', 'echo hello world')
