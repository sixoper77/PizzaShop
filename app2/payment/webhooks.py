import os

import requests
import stripe
import stripe.error
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from main.models import Products
from orders.models import Order

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVereficationError as e:
        return HttpResponse(status=400)
    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            try:
                requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": order.telegram_id,
                        "text": f"✅ Оплата за заказ #{order.id} прошла успешно!",
                    },
                )
            except Exception as e:
                print(e)

    return HttpResponse(status=200)
