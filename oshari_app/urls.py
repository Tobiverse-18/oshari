from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, ProductSitemap

from .views import (
    paystack_webhook,
)

sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
}

urlpatterns = [

    # ==========================================
    # WEBSITE
    # ==========================================

    path("", views.home, name="home"),
    path("shop/", views.shop, name="shop"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),

    # ==========================================
    # PRODUCTS
    # ==========================================

    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),

    # ==========================================
    # NEWSLETTER
    # ==========================================

    path("newsletter/subscribe/", views.subscribe_newsletter, name="newsletter_subscribe"),
    path("newsletter/subscribe/", views.subscribe_newsletter, name="subscribe_newsletter"),

    # ==========================================
    # CART
    # ==========================================

    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/", views.update_cart, name="update_cart"),

    # ==========================================
    # CHECKOUT
    # ==========================================

    path("checkout/", views.checkout, name="checkout"),

    # ==========================================
    # PAYMENTS
    # ==========================================

    path("payment/<int:order_id>/", views.payment, name="payment"),
    path("payment/<int:order_id>/initialize/", views.initialize_payment, name="initialize_payment"),
    path("payment/verify/<str:reference>/", views.verify_payment, name="verify_payment"),
    path("payment/success/<int:order_id>/", views.payment_success, name="payment_success"),
    path("payment/failed/", views.payment_failed, name="payment_failed"),

    # ==========================================
    # ORDER TRACKING
    # ==========================================

    path("track-order/", views.track_order, name="track_order"),

    # ==========================================
    # DASHBOARD AUTH
    # ==========================================

    path("dashboard/login/", views.dashboard_login, name="dashboard_login"),
    path("dashboard/logout/", views.dashboard_logout, name="dashboard_logout"),

    # ==========================================
    # DASHBOARD HOME
    # ==========================================

    path("dashboard/", views.dashboard, name="dashboard"),

    # ==========================================
    # DASHBOARD PRODUCTS
    # ==========================================

    path("dashboard/products/", views.dashboard_products, name="dashboard_products"),
    path("dashboard/products/add/", views.dashboard_add_product, name="dashboard_add_product"),
    path("dashboard/products/edit/<int:product_id>/", views.dashboard_edit_product, name="dashboard_edit_product"),
    path("dashboard/products/delete/<int:product_id>/", views.dashboard_delete_product, name="dashboard_delete_product"),

    # ==========================================
    # DASHBOARD ORDERS
    # ==========================================

    path("dashboard/orders/", views.dashboard_orders, name="dashboard_orders"),

    # ==========================================
    # DASHBOARD NEWSLETTER
    # ==========================================

    path("dashboard/newsletter/", views.dashboard_newsletter, name="dashboard_newsletter"),
    path(
    "dashboard/newsletter/delete/<int:subscriber_id>/", views.dashboard_delete_subscriber, name="dashboard_delete_subscriber",),

    # ==========================================
    # DASHBOARD CONTACTS
    # ==========================================

    path("dashboard/contacts/", views.dashboard_contacts, name="dashboard_contacts"),
    path("dashboard/contacts/view/<int:contact_id>/", views.dashboard_contact_detail, name="dashboard_contact_detail",),
    path("dashboard/contacts/delete/<int:contact_id>/", views.dashboard_delete_contact, name="dashboard_delete_contact",),

    # ==========================================
    # DASHBOARD SETTINGS
    # ==========================================

    path("dashboard/settings/", views.dashboard_settings, name="dashboard_settings"),

    path(
    "dashboard/gallery/delete/<int:image_id>/",
    views.dashboard_delete_gallery_image,
    name="dashboard_delete_gallery_image",
    ),

    path(
        "dashboard/orders/<int:order_id>/",
        views.dashboard_order_detail,
        name="dashboard_order_detail",
    ),

    # ALL YOUR EXISTING URLS HERE

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),

    path("robots.txt", views.robots_txt, name="robots_txt"),

    path("payment/webhook/", paystack_webhook, name="paystack_webhook"),

]

