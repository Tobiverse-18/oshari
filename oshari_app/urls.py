from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("newsletter/subscribe/", views.subscribe_newsletter, name="newsletter_subscribe",),
    path("product/<int:pk>/", views.product_detail, name="product_detail",),
]