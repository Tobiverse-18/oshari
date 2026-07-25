from django.shortcuts import render
from .models import Product


from django.http import HttpResponse

def home(request):
    return render(request, "home/home.html")