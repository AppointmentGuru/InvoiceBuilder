from django.contrib import admin
from .models import Invoice, InvoiceSettings, Payment, ProofOfPayment

class PaymentAdmin(admin.ModelAdmin):    
    list_display = ('practitioner_id', 'customer_id', 'payment_date', 'invoice', 'currency', 'amount',)
    list_filter = ('practitioner_id', 'payment_method', )


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'practitioner_id', 'customer_id', 'sender_email', 'date', 'due_date', 'currency', 'invoice_amount', 'amount_paid', 'status')
    list_filter = ('practitioner_id', 'status',)

class InvoiceSettingsAdmin(admin.ModelAdmin):
    list_display = ('id',
        'practitioner_id',
        'quote_notes',
        'invoice_notes',
        'receipt_notes',
        'billing_address',
        'customer_info',
        'lineitem_template',
        'include_booking_info',
        'integrate_medical_aid',
        'show_snapcode_on_invoice',
        'allow_pre_payments',
        'allow_submit_to_medical_aid',
        'include_vat',
        'snap_id',
        'vat_percent'
    )

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceSettings, InvoiceSettingsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ProofOfPayment)