import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# 4242 4242 4242 4242 - Use this card number to simulate a successful payment

def process_payment_stripe(amount, payment_method):
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100), # ammount in cents
            currency="usd",
            payment_method_types=["card"],
            receipt_email="customer@example.com"
        )
        return {
            "transaction_id": intent["id"],
            "status": "completed"
        }
    except stripe.error.StripeError as e:
        return {
            "status": "failed"
        }