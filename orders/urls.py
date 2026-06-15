from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_orders, name="order-list"),
    path("create/", views.create_order, name="order-create"),
]
