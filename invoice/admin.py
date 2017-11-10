from django.contrib import admin
from .models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'practitioner_id', 'customer_id', 'date', 'due_date', 'currency', 'invoice_amount', 'amount_paid', 'status')


admin.site.register(Invoice, InvoiceAdmin)
