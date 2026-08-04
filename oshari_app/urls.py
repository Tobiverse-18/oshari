from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("newsletter/subscribe/", views.subscribe_newsletter, name="newsletter_subscribe",),
    path("newsletter/subscribe/", views.subscribe_newsletter, name="subscribe_newsletter",),
    path("product/<int:pk>/", views.product_detail, name="product_detail",),
    path("shop/", views.shop, name="shop"),
    path("cart/",views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/", views.update_cart, name="update_cart",),
    path("checkout/", views.checkout, name="checkout",),
    path("payment/<int:order_id>/", views.payment, name="payment",),
    path("payment/<int:order_id>/initialize/", views.initialize_payment, name="initialize_payment",),
    path("payment/verify/<str:reference>/", views.verify_payment, name="verify_payment",),
    path("payment/success/<int:order_id>/", views.payment_success, name="payment_success",),
    path("payment/failed/", views.payment_failed, name="payment_failed",),
    path("track-order/", views.track_order, name="track_order",),
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now",),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact",),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy",),
]