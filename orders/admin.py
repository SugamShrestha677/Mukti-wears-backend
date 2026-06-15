from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "price", "quantity", "size", "colour")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "subtotal", "created_at")
    list_filter = ("status", "payment_method")
    search_fields = ("order_number", "user__email")
    inlines = [OrderItemInline]
