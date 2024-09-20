from django.urls import path

from .views import *

urlpatterns = [
    path("<int:id>/get_shipping_rates/", get_shipping_rates, name="get-shipping-rates"),
    path("<int:id>/schedule_delivery/", schedule_delivery, name="schedule-delivery"),
    path("<int:id>/change_status/", change_delivery_status, name="change-delivery-status"),
    path("<int:id>/check_status/", check_delivery_status, name="check-delivery-status")
]