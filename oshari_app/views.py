from django.shortcuts import render
from .models import Product

def home(request):
    new_drops = Product.objects.filter(
        is_available=True,
        is_new_drop=True
    )[:8]

    context = {
        "new_drops": new_drops,
    }

    return render(request, "home/home.html", context)