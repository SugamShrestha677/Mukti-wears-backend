from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_view, name="cart-detail"),
    path("items/", views.cart_add_item, name="cart-add-item"),
    path("items/<int:item_id>/", views.cart_update_item, name="cart-update-item"),
    path("items/<int:item_id>/delete/", views.cart_remove_item, name="cart-remove-item"),
]
