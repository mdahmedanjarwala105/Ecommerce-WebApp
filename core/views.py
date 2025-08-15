from uuid import UUID
from decimal import Decimal, ROUND_HALF_UP
import stripe
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from store.models import Cart, CartItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def _to_minor(amount: Decimal) -> int:
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


@require_POST
def start_checkout(request: HttpRequest, cart_id: UUID):
    cart = get_object_or_404(Cart, pk=cart_id)
    items = CartItem.objects.select_related("product").filter(cart=cart)
    if not items:
        return HttpResponseBadRequest("Cart is empty.")

    success_url = (
        request.build_absolute_uri(reverse("core:success"))
        + "?session_id={CHECKOUT_SESSION_ID}"
    )

    line_items = [
        {
            "price_data": {
                "currency": settings.STRIPE_CURRENCY,
                "product_data": {"name": i.product.title},
                "unit_amount": _to_minor(i.product.price),
            },
            "quantity": i.quantity,
        }
        for i in items
    ]

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=line_items,
        success_url=success_url,
    )
    return redirect(session.url, permanent=False)


def success(request: HttpRequest) -> HttpResponse:
    return HttpResponse("✅ Payment successful!")
