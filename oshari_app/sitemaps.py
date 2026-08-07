from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class StaticViewSitemap(Sitemap):

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "shop",
            "about",
            "contact",
            "privacy_policy",
            "track_order",
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_available=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("product_detail", args=[obj.id])