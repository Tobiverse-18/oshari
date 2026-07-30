from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Product, NewsletterSubscriber
from .forms import NewsletterForm


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


from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk,
        is_available=True
    )

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
        },
    )