from django.shortcuts import render
from .models import Product


from django.http import HttpResponse

def home(request):
    return HttpResponse("OSHARI is working!")