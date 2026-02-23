from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['project', 'amount', 'payment_date', 'payment_method', 'transaction_id']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['project__project_name', 'transaction_id']
