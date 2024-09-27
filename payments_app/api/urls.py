from django.urls import path

from .views import *

urlpatterns = [
    path("order/<int:id>/", process_payment, name="process-payment"),
    path("order/status/<int:pk>/", PaymentDetailView.as_view(), name="get-payment-status")
]