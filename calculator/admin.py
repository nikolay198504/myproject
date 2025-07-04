from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'amount', 'customer_phone', 'customer_email', 'paid_at', 'type')
    search_fields = ("order_id", "customer_email", "customer_phone")
    list_filter = ("status", "paid_at")