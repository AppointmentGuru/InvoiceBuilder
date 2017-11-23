'''
API for AppointmentGuru microservices
'''
import requests, json
from django.conf import settings
from pubsub import get_backend

def publish(key, payload):
    '''Send a message onward'''
    pubsub = get_backend(
        settings.PUB_SUB_BACKEND[0],
        settings.PUB_SUB_BACKEND[1],
        settings.PUB_SUB_CHANNEL)
    return pubsub.publish(key, payload)

def get_headers(user_id, consumer='appointmentguru'):
    return {
        'X_ANONYMOUS_CONSUMER': 'False',
        'X_AUTHENTICATED_USERID': str(user_id),
        'X_CONSUMER_USERNAME': consumer,
    }

def send_invoice(invoice, to_email=None, to_phone=None):
    '''
    Sends invoice to to_email and to_phone if they are available.
    if neither is available, then the
    '''
    url = '{}/communications/'.format(settings.COMMUNICATIONGURU_API)

    # invoice_url = "{}/invoice/{}/?key={}"\
    #                 .format(settings.INVOICEGURU_BASE_URL,
    #                         invoice.id,
    #                         invoice.password)
    invoice_url = invoice.admin_invoice_url
    invoice_date = invoice.context.get('due_date')
    practice_name = invoice.context.get('practice_name', '')
    subject = 'Your invoice from {} for {}'.format(practice_name, invoice_date)
    if invoice.status == 'paid':
        subject = 'Your receipt'

    short_message = subject
    message = """Hi

Attached please find your invoice for {}.
You can also view it online at:
{}
""".format(invoice_date, invoice_url)

    object_ids = [
        'user:{}'.format(invoice.practitioner_id),
        'user:{}'.format(invoice.customer_id)
    ]
    object_ids = object_ids + invoice.object_ids

    from_email = invoice.sender_email
    short_message = "{}. {}".format(short_message, invoice.get_short_url())
    data = {
        "owner": invoice.practitioner_id,
        "object_ids": object_ids,
        "subject": subject,
        "message": message,
        "short_message": short_message,
        "attached_urls": [invoice_url],
        "sender_email": from_email
    }
    total_recipients = []
    if to_email is not None:
        data.update({
            "preferred_transport": "email",
            "recipient_emails": [to_email],
        })
        total_recipients.append(to_email)
    if to_phone is not None:
        data.update({
            "recipient_phone_number": to_phone,
            "preferred_transport": "sms",
        })
        total_recipients.append(to_phone)

    if len(total_recipients) > 0:
        return requests.post(
            url,
            json=data,
            headers=get_headers(invoice.practitioner_id))
    return None
