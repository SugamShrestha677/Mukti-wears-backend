from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id", "product_name", "product_image", "price",
            "quantity", "size", "colour",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "order_number", "status", "shipping_name",
            "shipping_address", "shipping_city", "shipping_phone",
            "payment_method", "subtotal", "items", "created_at",
        )
        read_only_fields = ("id", "order_number", "status", "subtotal", "created_at")


class CreateOrderSerializer(serializers.Serializer):
    """Input serializer for creating an order from the user's current cart."""
    shipping_name = serializers.CharField(max_length=200)
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField(max_length=100)
    shipping_phone = serializers.CharField(max_length=20)
    payment_method = serializers.CharField(max_length=20, default="cod")
