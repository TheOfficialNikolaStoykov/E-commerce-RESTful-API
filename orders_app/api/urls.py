from django.urls import path

from .views import *

urlpatterns = [
    path("", list_orders_view, name="orders"),
    path("my-orders/", view_orders_view, name="orders-view-user"),
    path("admin/<int:pk>/", retrieve_single_order_view_admin, name="order-single-admin"),
    path("user/<int:pk>/", retrieve_single_order_view_user, name="order-single-user"),
    path("checkout/<int:pk>/", checkout_cart_view, name="cart-checkout"),
    path("<int:pk>/status/", change_order_status_view, name="order-change-status"),
]