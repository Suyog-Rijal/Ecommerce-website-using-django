import json
import uuid

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from Makeover.models import Order, OrderItem, Payment
from Authentication.models import UserModel
from Makeover.models import Product


def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart_data'))
        total_price = float(request.POST.get('checkout_price'))

        order = Order.objects.create(
            customer=request.user,
            total=total_price,
            status='pending'
        )

        for product_id, item in cart.items():
            product = Product.objects.get(id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )

        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                "price_data": {
                    "currency": "npr",
                    "product_data": {
                        "name": "Your Order",
                    },
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }],
            payment_method_types=["card"],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")) + f"?order_id={order.id}",
            cancel_url=request.build_absolute_uri(reverse("cancel")),
        )

        return redirect(checkout_session.url, code=303)

    return render(request, 'payment/cancel.html')


def success(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)

    if order:
        payment_exists = Payment.objects.filter(order=order, status='completed').exists()

        if not payment_exists:
            payment = Payment.objects.create(
                order=order,
                customer=order.customer,
                amount=order.total,
                payment_id=uuid.uuid4(),
                status='completed',
            )
            order.status = 'pending'
            order.save()

            payment.add_reward_points(reward_percent=5)

    return render(request, 'payment/success.html', {'order': order})



def cancel(request):
    return render(request, 'payment/cancel.html')
