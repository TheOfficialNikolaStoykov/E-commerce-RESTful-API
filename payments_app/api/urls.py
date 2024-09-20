from django.urls import path

from .views import *

urlpatterns = [
    path("order/<int:id>/", process_payment, name="process-payment"),
    path("order/status/<int:id>/", get_payment_status, name="get-payment-status")
]