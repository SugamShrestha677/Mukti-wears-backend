from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_view(request):
    """Get the current user's cart with all items."""
    cart = get_or_create_cart(request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cart_add_item(request):
    """Add an item to cart. If same product+size+colour exists, increment quantity."""
    cart = get_or_create_cart(request.user)
    serializer = CartItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    product_id = serializer.validated_data.get("product_id")
    size = serializer.validated_data["size"]
    colour = serializer.validated_data["colour"]
    quantity = serializer.validated_data.get("quantity", 1)

    # Try to find existing item with same product+size+colour
    try:
        item = CartItem.objects.get(
            cart=cart, product_id=product_id, size=size, colour=colour
        )
        item.quantity += quantity
        item.save()
    except CartItem.DoesNotExist:
        item = CartItem.objects.create(
            cart=cart,
            product_id=product_id,
            size=size,
            colour=colour,
            quantity=quantity,
        )

    return Response(
        CartItemSerializer(item).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def cart_update_item(request, item_id):
    """Update quantity of a cart item."""
    cart = get_or_create_cart(request.user)
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND
        )

    quantity = request.data.get("quantity")
    if quantity is not None:
        quantity = int(quantity)
        if quantity <= 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        item.quantity = quantity
        item.save()

    return Response(CartItemSerializer(item).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def cart_remove_item(request, item_id):
    """Remove an item from cart."""
    cart = get_or_create_cart(request.user)
    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND
        )
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
