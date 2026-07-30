from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Product, NewsletterSubscriber
from .forms import NewsletterForm
from .cart import Cart


# ==========================================
# HOME
# ==========================================

def home(request):

    new_drops = Product.objects.filter(
        is_available=True,
        is_new_drop=True
    )[:8]

    form = NewsletterForm()

    context = {
        "new_drops": new_drops,
        "newsletter_form": form,
    }

    return render(
        request,
        "home/home.html",
        context,
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


def remove_from_cart(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id,
    )

    cart.remove(product)

    return redirect("cart")


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