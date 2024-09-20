from django.urls import path

from .views import *

urlpatterns = [
    path("", view_cart_view, name="cart"),
    path("cart_item/add/", add_cart_item_view, name="cart-add"),
    path("cart_item/edit/<int:pk>/", edit_cart_item_view, name="cart_item-edit"),
    path("cart_item/delete/<int:pk>/", delete_cart_item_view, name="cart_item-delete"),
    path("clear/", clear_cart_items_view, name="cart-clear"),
]