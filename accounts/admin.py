from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'phone_number', 'created_at']
    search_fields = ['user__username', 'user__email', 'company_name']
    list_filter = ['created_at']
