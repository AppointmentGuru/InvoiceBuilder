# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.test import TestCase, override_settings
from django.conf import settings

from api.testutils import (
    create_mock_invoice,
    create_mock_v2_invoice
)
from .responses import (
    expect_get_practitioner_response,
    expect_get_user_response,
    expect_get_record_response,
    expect_get_appointments
)
from ..models import Transaction, Invoice

import responses

class InvoiceSubmitViewTestCase(TestCase):

    def setUp(self):
        self.invoice = create_mock_invoice()
        self.url = '/invoice/submit/{}/?key={}'.format(
            self.invoice.id,
            self.invoice.password
        )

    # def test_load_with_existing_record(self):
    #     res = self.client.get(self.url)


class InvoiceViewTestCase(TestCase):

    def setUp(self):
        self.invoice = create_mock_invoice()
        self.url = reverse('invoice_view', args=(self.invoice.pk,))

    def test_get_without_password(self):
        self.result = self.client.get(self.url)
        assert self.result.status_code == 404,\
            'Expected 404 when accessing invoice view page without password'

    def test_get_with_password(self):
        url = '{}?key={}'.format(self.url, self.invoice.password)
        self.result = self.client.get(url)
        assert self.result.status_code == 200

    def test_get_with_customer_password(self):
        '''When getting the page with the customer password, set views = True'''
        print ('TBD')

class SnapScanInvoiceWebHookTestCase(TestCase):

    @responses.activate
    @override_settings(COMMUNICATIONGURU_API='https://communicationguru')
    @override_settings(KEEN_PROJECT_ID='1234')
    def setUp(self):
        '''
        curl -i -X POST -d 'payload="{\"id\":7,\"status\":\"completed\",\"totalAmount\":1000,\"tipAmount\":0,\"feeAmount\":35,\"settleAmount\":965,\"requiredAmount\":1000,\"date\":\"2018-04-23T13:51:59Z\",\"snapCode\":\"EJrKB_SJ\",\"snapCodeReference\":\"587e9743-3c7c-4e86-b54c-985ca29fe895\",\"userReference\":\"\",\"merchantReference\":\"1765\",\"statementReference\":null,\"authCode\":\"455303\",\"deliveryAddress\":null,\"extra\":{\"amount\":\"1000\",\"invoice_id\":\"1790\"}}"' https://invoiceguru.appointmentguru.co/incoming/snapscan/739B7B5E-B896-4C99-9AF5-AD424DB437A5/
        curl -i -X POST -d 'payload={\"id\":7,\"status\":\"completed\",\"totalAmount\":1000,\"tipAmount\":0,\"feeAmount\":35,\"settleAmount\":965,\"requiredAmount\":1000,\"date\":\"2018-04-23T13:51:59Z\",\"snapCode\":\"EJrKB_SJ\",\"snapCodeReference\":\"587e9743-3c7c-4e86-b54c-985ca29fe895\",\"userReference\":\"\",\"merchantReference\":\"1765\",\"statementReference\":null,\"authCode\":\"455303\",\"deliveryAddress\":null,\"extra\":{\"amount\":\"1000\",\"invoice_id\":\"1790\"}}' http://localhost:8000/incoming/snapscan/739B7B5E-B896-4C99-9AF5-AD424DB437A5/
        '''
        keen_url = 'https://api.keen.io/3.0/projects/{}/events/snapscan_webhook'.format(settings.KEEN_PROJECT_ID)
        self.p_id = 1
        self.u_id = 2
        responses.add(
            responses.POST,
            url=keen_url,
            json={'ok': 'true'}
        )
        responses.add(
            responses.POST,
            url='https://communicationguru/communications/',
            json={"id": 1},
            status=201
        )
        expect_get_practitioner_response(practitioner_id = self.p_id)
        expect_get_user_response(user_id=self.u_id)
        expect_get_record_response(self.u_id, self.p_id)
        expect_get_appointments([1], self.p_id)

        self.url = reverse('incoming_snapscan')
        self.invoice = Invoice()
        self.invoice.practitioner_id = self.p_id
        self.invoice.customer_id = self.u_id
        self.invoice.appointments = [1]
        self.invoice.save()
        data = {
            "payload": "{\"id\":7,\"status\":\"completed\",\"totalAmount\":1000,\"tipAmount\":0,\"feeAmount\":35,\"settleAmount\":965,\"requiredAmount\":1000,\"date\":\"2018-04-23T13:51:59Z\",\"snapCode\":\"EJrKB_SJ\",\"snapCodeReference\":\"587e9743-3c7c-4e86-b54c-985ca29fe895\",\"userReference\":\"\",\"merchantReference\":\"1765\",\"statementReference\":null,\"authCode\":\"455303\",\"deliveryAddress\":null,\"extra\":{\"amount\":\"1000\",\"invoiceId\":\""+str(self.invoice.id)+"\"}}"
        }
        self.result = self.client.post(self.url, data)
        self.invoice.refresh_from_db()

        num_calls = len(responses.calls)
        assert num_calls == 2,\
            'Expected 1 calls. Got: {}'.format(num_calls)

        self.keen_request = responses.calls[0].request
        self.comms_request = responses.calls[1].request

    def test_returns_ok(self):
        assert self.result.status_code == 200

    def test_it_publishes_the_result(self):
        # not sure how to test this
        pass

    def test_updates_invoice_status(self):
        self.invoice.refresh_from_db()
        assert self.invoice.status == 'paid'

    def test_it_creates_a_transaction(self):
        assert Transaction.objects.count() == 2

    def test_amount_due_is_zero(self):
        self.invoice.refresh_from_db()
        assert self.invoice.amount_due == 0,\
            'Expected amount_due to be 0. got: {}'.format(self.invoice.amount_due)

    def test_it_tags_the_payment_as_snapscan(self):
        pass

    def test_it_sends_a_receipt(self):
        pass

class SnapScanAppointmentWebHookTestCase(TestCase):

    def setUp(self):
        pass