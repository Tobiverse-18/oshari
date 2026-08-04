from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, request
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Product, NewsletterSubscriber
from .forms import NewsletterForm
from .cart import Cart

from decimal import Decimal

from .models import Order, OrderItem
from .forms import CheckoutForm

import requests
from django.conf import settings

from .emails import (
    send_order_confirmation,
    send_admin_notification,
)

from .forms import ContactForm

from django.contrib import messages


# ==========================================
# HOME
# ==========================================

def home(request):

    new_drops = Product.objects.filter(

        is_available=True,

        is_new_drop=True

    )[:4]

    return render(

        request,

        "home/home.html",

        {

            "new_drops": new_drops,

        },

    )


# ==========================================
# NEWSLETTER
# ==========================================

@require_POST
def subscribe_newsletter(request):

    email = request.POST.get("email")

    if not email:

        return JsonResponse({
            "success": False,
            "message": "Please enter your email."
        })

    if NewsletterSubscriber.objects.filter(email=email).exists():

        return JsonResponse({
            "success": False,
            "message": "You're already subscribed."
        })

    NewsletterSubscriber.objects.create(email=email)

    return JsonResponse({
        "success": True,
        "message": "Thanks for subscribing!"
    })


# ==========================================
# SHOP
# ==========================================

def shop(request):

    search = request.GET.get("search", "")

    products = Product.objects.filter(
        is_available=True
    )

    if search:

        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        "products": products,
        "search": search,
    }

    return render(
        request,
        "products/shop.html",
        context,
    )


# ==========================================
# PRODUCT DETAIL
# ==========================================

def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        is_available=True,
    )

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
        },
    )


# ==========================================
# CART
# ==========================================

from django.views.decorators.http import require_POST
from django.http import JsonResponse


@require_POST
def add_to_cart(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
    )

    if product.track_stock and product.stock <= 0:
        return JsonResponse({
            "success": False,
            "message": "Sorry, this product is out of stock."
        })

    quantity = int(request.POST.get("quantity", 1))

    cart.add(
        product=product,
        quantity=quantity,
    )

    return JsonResponse({
        "success": True,
        "product": product.name,
        "quantity": quantity,
        "cart_count": cart.get_total_items(),
    })


def cart_detail(request):

    cart = Cart(request)

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
        },
    )


@require_POST
def remove_from_cart(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    cart.remove(product)

    return JsonResponse({
        "success": True,
        "total": cart.get_total_price(),
        "items": cart.get_total_items(),
        "empty": cart.get_total_items() == 0,
    })


@require_POST
def update_cart(request):

    product_id = request.POST.get("product_id")

    quantity = int(request.POST.get("quantity"))

    cart = Cart(request)

    product = get_object_or_404(

        Product,

        id=product_id

    )

    cart.update(

        product,

        quantity

    )

    subtotal = product.price * quantity

    return JsonResponse({

        "success": True,

        "subtotal": subtotal,

        "total": cart.get_total_price(),

        "items": cart.get_total_items()

    })


def checkout(request):

    cart = Cart(request)

    buy_now = request.session.get("buy_now")

    checkout_items = []
    total = Decimal("0.00")

    if buy_now:

        product = get_object_or_404(
            Product,
            id=buy_now["product_id"],
            is_available=True,
        )

        quantity = buy_now["quantity"]

        item_total = product.price * quantity

        checkout_items.append({
            "product": product,
            "quantity": quantity,
            "total_price": item_total,
        })

        total = item_total

    else:

        if len(cart.cart) == 0:

            return redirect("shop")

        checkout_items = list(cart)

        total = cart.get_total_price()

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.total = total

            order.save()

            order.order_number = f"OSH{order.id:06d}"

            order.save(update_fields=["order_number"])

            for item in checkout_items:

                OrderItem.objects.create(

                    order=order,

                    product=item["product"],

                    quantity=item["quantity"],

                    price=item["product"].price,

                )

            if buy_now:

                del request.session["buy_now"]

            return redirect("payment", order.id)

    else:

        form = CheckoutForm()

    return render(

        request,

        "checkout/checkout.html",

        {

            "form": form,

            "cart": checkout_items,

            "total": total,

            "buy_now": bool(buy_now),

        },

    )



def payment(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id

    )

    return render(

        request,

        "checkout/payment.html",

        {

            "order": order,

        },

    )


from django.shortcuts import redirect
import requests
from django.conf import settings


def initialize_payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": order.email,
        "amount": int(order.total * 100),   # Kobo
        "reference": order.order_number,
        "callback_url": request.build_absolute_uri(
            f"/payment/verify/{order.order_number}/"
        ),
    }

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=data,
        headers=headers,
    )

    result = response.json()

    if result["status"]:

        return redirect(result["data"]["authorization_url"])

    return redirect("payment", order.id)


def verify_payment(request, reference):

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers=headers,
    )

    result = response.json()

    if (
        result["status"] and
        result["data"]["status"] == "success"
    ):

        order = get_object_or_404(
            Order,
            order_number=reference
        )

        if not order.paid:

            order.paid = True
            order.status = "Paid"
            order.save(update_fields=["paid", "status"])
            send_order_confirmation(order)
            send_admin_notification(order)

            # Empty the customer's cart
            cart = Cart(request)
            cart.clear()

        return redirect("payment_success", order.id)

    return redirect("payment_failed")

def payment_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "checkout/payment_success.html",
        {
            "order": order,
        },
    )


def payment_failed(request):

    return render(
        request,
        "checkout/payment_failed.html",
    )


def track_order(request):

    order = None
    searched = False

    order_number = request.GET.get("order")

    if order_number:
        searched = True

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            order = None

    return render(
        request,
        "orders/track_order.html",
        {
            "order": order,
            "searched": searched,
        },
    )


@require_POST
def buy_now(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
    )

    if product.track_stock and product.stock <= 0:
        return redirect("product_detail", pk=product.id)

    quantity = int(request.POST.get("quantity", 1))

    request.session["buy_now"] = {
        "product_id": product.id,
        "quantity": quantity,
    }

    return redirect("checkout")


def about(request):
    return render(request, "about/about.html")


from django.contrib import messages

def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Thank you! Your message has been sent successfully. We'll reply as soon as possible."
            )

            return redirect("contact")

    else:

        form = ContactForm()

    return render(
        request,
        "contact/contact.html",
        {
            "form": form,
        },
    )


def privacy_policy(request):

    return render(

        request,

        "pages/privacy_policy.html",

    )