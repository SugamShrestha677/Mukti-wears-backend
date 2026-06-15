from rest_framework import serializers
from .models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "price", "image",
            "category", "series", "sizes", "colours",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id", "name", "slug", "description", "story", "care",
            "price", "stock", "image", "category", "series",
            "sizes", "colours", "is_active", "created_at",
        )
