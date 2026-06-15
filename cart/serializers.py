from rest_framework import serializers
from products.serializers import ProductListSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True, required=False)
    product_slug = serializers.SlugField(write_only=True, required=False)

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_id", "product_slug", "quantity", "size", "colour")
        read_only_fields = ("id",)

    def validate(self, attrs):
        # Resolve product by slug if provided (frontend uses slugs as IDs)
        if "product_slug" in attrs:
            from products.models import Product
            try:
                product = Product.objects.get(slug=attrs.pop("product_slug"), is_active=True)
                attrs["product_id"] = product.id
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product_slug": "Product not found."})
        elif "product_id" not in attrs and not self.instance:
            raise serializers.ValidationError("product_slug or product_id is required.")
        return attrs


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    count = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "items", "count", "subtotal")

    def get_count(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_subtotal(self, obj):
        total = sum(
            item.product.price * item.quantity
            for item in obj.items.select_related("product").all()
        )
        return float(total)
