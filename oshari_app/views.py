from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, request
from django.views.decorators.http import require_POST
from django.db.models import Q
from .emails import send_contact_notification

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

from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import (
    Product,
    Order,
    NewsletterSubscriber,
    ContactMessage,
)

from django.contrib import messages
from django.shortcuts import redirect

from django.http import HttpResponse


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

    email = request.POST.get("email", "").strip().lower()

    if not email:
        return JsonResponse({
            "success": False,
            "message": "Please enter your email."
        }, status=400)

    try:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email
        )

        if not created:
            return JsonResponse({
                "success": False,
                "message": "You're already subscribed."
            }, status=200)

        return JsonResponse({
            "success": True,
            "message": "Thanks for subscribing!"
        }, status=200)

    except Exception:
        return JsonResponse({
            "success": False,
            "message": "Something went wrong. Please try again later."
        }, status=500)


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

    # ==========================================
    # STOCK CHECK
    # ==========================================

    if product.track_stock and product.stock <= 0:

        return JsonResponse({
            "success": False,
            "message": "Sorry, this product is out of stock."
        })

    # ==========================================
    # QUANTITY
    # ==========================================

    try:

        quantity = int(
            request.POST.get("quantity", 1)
        )

    except (TypeError, ValueError):

        quantity = 1

    if quantity < 1:

        quantity = 1

    # ==========================================
    # SIZE
    # ==========================================

    size = request.POST.get(
        "size",
        ""
    ).strip()

    # ==========================================
    # REQUIRE SIZE IF PRODUCT HAS SIZES
    # ==========================================

    if product.sizes.exists() and not size:

        return JsonResponse({
            "success": False,
            "message": "Please select a size."
        })

    # ==========================================
    # VALIDATE SIZE
    # ==========================================

    if size and not product.sizes.filter(
        size=size
    ).exists():

        return JsonResponse({
            "success": False,
            "message": "Invalid size selected."
        })

    # ==========================================
    # ADD TO CART
    # ==========================================

    cart.add(
        product=product,
        quantity=quantity,
        size=size or None,
    )

    # ==========================================
    # RESPONSE
    # ==========================================

    return JsonResponse({

        "success": True,

        "product": product.name,

        "quantity": quantity,

        "size": size or None,

        "cart_count":
            cart.get_total_items(),

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

    size = request.POST.get(
        "size",
        ""
    ).strip()

    cart.remove(
        product=product,
        size=size or None,
    )

    return JsonResponse({

        "success": True,

        "total": str(
            cart.get_total_price()
        ),

        "items":
            cart.get_total_items(),

        "empty":
            cart.get_total_items() == 0,

    })


@require_POST
def update_cart(request):

    product_id = request.POST.get("product_id")
    quantity_raw = request.POST.get("quantity")
    size = request.POST.get("size", "").strip()

    # ==========================================
    # VALIDATE QUANTITY
    # ==========================================

    try:
        quantity = int(quantity_raw)
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    # ==========================================
    # CART
    # ==========================================

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True,
    )

    # ==========================================
    # UPDATE PRODUCT + SIZE
    # ==========================================

    cart.update(
        product=product,
        quantity=quantity,
        size=size or None,
    )

    # ==========================================
    # RESPONSE
    # ==========================================

    subtotal = product.price * quantity

    return JsonResponse({

        "success": True,

        "subtotal": str(subtotal),

        "total": str(
            cart.get_total_price()
        ),

        "items":
            cart.get_total_items(),

    })


def checkout(request):

    cart = Cart(request)

    buy_now = request.session.get("buy_now")

    checkout_items = []
    total = Decimal("0.00")

    # ==========================================
    # BUY NOW
    # ==========================================

    if buy_now:

        product = get_object_or_404(
            Product,
            id=buy_now["product_id"],
            is_available=True,
        )

        quantity = buy_now["quantity"]

        size = buy_now.get("size")

        item_total = product.price * quantity

        checkout_items.append({
            "product": product,
            "quantity": quantity,
            "size": size,
            "total_price": item_total,
        })

        total = item_total

    # ==========================================
    # NORMAL CART CHECKOUT
    # ==========================================

    else:

        if len(cart.cart) == 0:

            return redirect("shop")

        checkout_items = list(cart)

        total = cart.get_total_price()

    # ==========================================
    # CREATE ORDER
    # ==========================================

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.total = total

            order.save()

            order.order_number = f"OSH{order.id:06d}"

            order.save(
                update_fields=["order_number"]
            )

            # ==========================================
            # CREATE ORDER ITEMS
            # ==========================================

            for item in checkout_items:

                OrderItem.objects.create(

                    order=order,

                    product=item["product"],

                    size=item.get("size"),

                    quantity=item["quantity"],

                    price=item["product"].price,

                )

            # ==========================================
            # CLEAR BUY NOW
            # ==========================================

            if buy_now:

                del request.session["buy_now"]

            return redirect(
                "payment",
                order.id
            )

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

import hashlib
import hmac
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def paystack_webhook(request):

    if request.method != "POST":
        return JsonResponse(
            {"message": "Method not allowed"},
            status=405
        )

    # Get Paystack signature
    signature = request.headers.get("x-paystack-signature")

    if not signature:
        return JsonResponse(
            {"message": "Missing signature"},
            status=400
        )

    # Verify that the request really came from Paystack
    computed_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode("utf-8"),
        request.body,
        hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(
        computed_signature,
        signature
    ):
        return JsonResponse(
            {"message": "Invalid signature"},
            status=400
        )

    try:

        payload = json.loads(request.body)

    except json.JSONDecodeError:

        return JsonResponse(
            {"message": "Invalid JSON"},
            status=400
        )

    # Only process successful charges
    if payload.get("event") == "charge.success":

        reference = payload.get("data", {}).get("reference")

        if reference:

            try:

                order = Order.objects.get(
                    order_number=reference
                )

                if not order.paid:

                    order.paid = True
                    order.status = "Paid"

                    order.save(
                        update_fields=[
                            "paid",
                            "status"
                        ]
                    )

                    send_order_confirmation(order)
                    send_admin_notification(order)

            except Order.DoesNotExist:

                pass

    return JsonResponse(
        {"status": "success"}
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

        return redirect(
            "product_detail",
            pk=product.id
        )

    quantity = int(
        request.POST.get("quantity", 1)
    )

    size = request.POST.get("size")

    if product.sizes.exists() and not size:

        messages.error(
            request,
            "Please select a size."
        )

        return redirect(
            "product_detail",
            pk=product.id
        )

    request.session["buy_now"] = {

        "product_id": product.id,

        "quantity": quantity,

        "size": size,

    }

    return redirect("checkout")


def about(request):
    return render(request, "about/about.html")


from django.contrib import messages

def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            contact = form.save()

            # Send email notification to admin
            send_contact_notification(contact)

            messages.success(
                request,
                "Thank you! Your message has been sent successfully. We'll reply as soon as possible."
            )

            return redirect("contact")

        else:

            print(form.errors)

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


# ==========================================
# All my dashboard views start from here
# ==========================================

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.core.paginator import Paginator

from django.db.models import Sum

from .models import (
    Product,
    Order,
    NewsletterSubscriber,
    ContactMessage,
)

from .forms import ProductForm

from .models import ProductImage

from .models import ProductSize


# ==========================================
# DASHBOARD LOGIN
# ==========================================

def dashboard_login(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:

            login(request, user)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "dashboard/login.html",
    )


# ==========================================
# DASHBOARD LOGOUT
# ==========================================

@login_required
def dashboard_logout(request):

    logout(request)

    return redirect("dashboard_login")


# ==========================================
# DASHBOARD HOME
# ==========================================

@login_required
def dashboard(request):

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_subscribers = NewsletterSubscriber.objects.count()

    total_messages = ContactMessage.objects.count()

    total_revenue = (
        Order.objects
        .filter(paid=True)
        .aggregate(total=Sum("total"))
    )["total"] or 0

    recent_orders = Order.objects.order_by(
        "-created_at"
    )[:5]

    recent_messages = ContactMessage.objects.order_by(
        "-created_at"
    )[:5]

    context = {

        "total_products": total_products,

        "total_orders": total_orders,

        "total_subscribers": total_subscribers,

        "total_messages": total_messages,

        "total_revenue": total_revenue,

        "recent_orders": recent_orders,

        "recent_messages": recent_messages,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )


# ==========================================
# PRODUCTS
# ==========================================

@login_required
def dashboard_products(request):

    products = Product.objects.all().order_by(
        "-created_at"
    )

    q = request.GET.get("q")

    if q:

        products = products.filter(
            name__icontains=q
        )

    paginator = Paginator(products, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dashboard/products.html",
        {
            "products": page_obj,
            "page_obj": page_obj,
        },
    )


# ==========================================
# ADD PRODUCT
# ==========================================

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ProductForm
from .models import ProductImage
from .emails import send_new_product_notification


@login_required
def dashboard_add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            # ==========================================
            # SAVE PRODUCT + SIZES
            # ==========================================

            product = form.save()

            # ==========================================
            # SAVE GALLERY IMAGES
            # ==========================================

            gallery_images = request.FILES.getlist(
                "gallery_images"
            )

            for image in gallery_images:

                ProductImage.objects.create(
                    product=product,
                    image=image
                )

            # ==========================================
            # NEWSLETTER NOTIFICATION
            # ==========================================

            if product.notify_subscribers:

                send_new_product_notification(product)

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect(
                "dashboard_products"
            )

    else:

        form = ProductForm()

    return render(
        request,
        "dashboard/add_product.html",
        {
            "form": form,
        },
    )


# ==========================================
# EDIT PRODUCT
# ==========================================

@login_required
def dashboard_edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid():

            product = form.save()

            gallery_images = request.FILES.getlist(
                "gallery_images"
            )

            for image in gallery_images:

                ProductImage.objects.create(
                    product=product,
                    image=image,
                )

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "dashboard_products"
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "dashboard/edit_product.html",
        {
            "form": form,
            "product": product,
            "gallery": product.gallery.all(),
        },
    )


# ==========================================
# DELETE PRODUCT
# ==========================================

@login_required
def dashboard_delete_product(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect("dashboard_products")

    return render(
        request,
        "dashboard/delete_product.html",
        {
            "product": product,
        },
    )


# ==========================================
# ORDERS
# ==========================================

@login_required
def dashboard_orders(request):

    Order.objects.filter(
        is_read=False
    ).update(
        is_read=True
    )

    orders = Order.objects.all().order_by("-created_at")

    q = request.GET.get("q")

    if q:

        orders = orders.filter(
            order_number__icontains=q
        ) | Order.objects.filter(
            full_name__icontains=q
        )

    paginator = Paginator(orders, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dashboard/orders.html",
        {
            "orders": page_obj,
            "page_obj": page_obj,
        },
    )


@login_required
def dashboard_order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
    )

    if request.method == "POST":

        order.status = request.POST.get("status")

        order.save()

        messages.success(
            request,
            "Order updated successfully."
        )

        return redirect(
            "dashboard_order_detail",
            order_id=order.id,
        )

    order_items = order.items.all()

    return render(
        request,
        "dashboard/order_detail.html",
        {
            "order": order,
            "order_items": order_items,
        },
    )


# ==========================================
# NEWSLETTER
# ==========================================

@login_required
def dashboard_newsletter(request):

    NewsletterSubscriber.objects.filter(
        is_read=False
    ).update(
        is_read=True
    )

    subscribers = NewsletterSubscriber.objects.all().order_by("-subscribed_at")

    q = request.GET.get("q")

    if q:

        subscribers = subscribers.filter(
            email__icontains=q
        )

    paginator = Paginator(subscribers, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dashboard/newsletter.html",
        {
            "subscribers": page_obj,
            "page_obj": page_obj,
        },
    )


@login_required
def dashboard_delete_subscriber(request, subscriber_id):

    subscriber = get_object_or_404(
        NewsletterSubscriber,
        id=subscriber_id,
    )

    subscriber.delete()

    messages.success(
        request,
        "Subscriber deleted successfully.",
    )

    return redirect("dashboard_newsletter")


# ==========================================
# CONTACTS
# ==========================================

@login_required
def dashboard_contacts(request):

    ContactMessage.objects.filter(
        is_read=False
    ).update(
        is_read=True
    )

    contacts = ContactMessage.objects.all()

    q = request.GET.get("q")

    if q:

        contacts = contacts.filter(
            name__icontains=q
        ) | ContactMessage.objects.filter(
            email__icontains=q
        ) | ContactMessage.objects.filter(
            subject__icontains=q
        )

    paginator = Paginator(
        contacts.order_by("-created_at"),
        10
    )

    page = request.GET.get("page")

    page_obj = paginator.get_page(page)

    return render(
        request,
        "dashboard/contacts.html",
        {
            "contacts": page_obj,
            "page_obj": page_obj,
        },
    )

@login_required
def dashboard_contact_detail(request, contact_id):

    contact = get_object_or_404(
        ContactMessage,
        id=contact_id
    )

    if not contact.is_read:

        contact.is_read = True

        contact.save()

    return render(
        request,
        "dashboard/contact_detail.html",
        {
            "contact": contact
        }
    )

@login_required
def dashboard_delete_contact(request, contact_id):

    contact = get_object_or_404(
        ContactMessage,
        id=contact_id
    )

    contact.delete()

    messages.success(
        request,
        "Message deleted successfully."
    )

    return redirect(
        "dashboard_contacts"
    )


# ==========================================
# SETTINGS
# ==========================================

@login_required
def dashboard_settings(request):

    return render(
        request,
        "dashboard/settings.html",
    )

@login_required
def dashboard_delete_gallery_image(request, image_id):

    image = get_object_or_404(
        ProductImage,
        id=image_id,
    )

    product_id = image.product.id

    image.delete()

    messages.success(
        request,
        "Gallery image deleted successfully."
    )

    return redirect(
        "dashboard_edit_product",
        product_id=product_id,
    )


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")