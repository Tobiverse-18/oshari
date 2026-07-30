from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("newsletter/subscribe/", views.subscribe_newsletter, name="newsletter_subscribe",),
    path("product/<int:pk>/", views.product_detail, name="product_detail",),
    path("shop/", views.shop, name="shop"),
    path("cart/",views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/", views.update_cart, name="update_cart",),
]