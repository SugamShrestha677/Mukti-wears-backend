from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active", "created_at")
    list_filter = ("category", "is_active", "series")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
