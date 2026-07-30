from django.contrib import admin
from .models import NewsletterSubscriber
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "is_new_drop",
        "is_available",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_filter = (
        "is_new_drop",
        "is_available",
    )

    search_fields = (
        "name",
    )

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "subscribed_at",
    )

    search_fields = (
        "email",
    )

    ordering = (
        "-subscribed_at",
    )