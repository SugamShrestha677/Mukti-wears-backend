from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Create an order from the user's current cart."""
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        cart = Cart.objects.prefetch_related("items__product").get(user=request.user)
    except Cart.DoesNotExist:
        return Response(
            {"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST
        )

    cart_items = list(cart.items.select_related("product").all())
    if not cart_items:
        return Response(
            {"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Calculate subtotal
    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user,
            subtotal=subtotal,
            **serializer.validated_data,
        )

        # Snapshot cart items into order items
        order_items = []
        for item in cart_items:
            order_items.append(
                OrderItem(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    product_image=item.product.image,
                    price=item.product.price,
                    quantity=item.quantity,
                    size=item.size,
                    colour=item.colour,
                )
            )
        OrderItem.objects.bulk_create(order_items)

        # Clear the cart
        cart.items.all().delete()

    return Response(
        OrderSerializer(order).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_orders(request):
    """List all orders for the current user."""
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
