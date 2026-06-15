from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart({self.user})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20)
    colour = models.CharField(max_length=50)

    class Meta:
        unique_together = ["cart", "product", "size", "colour"]

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
