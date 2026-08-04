from django.contrib import admin

from .models import (
    Product,
    ProductImage,
    NewsletterSubscriber,
    Order,
    OrderItem,
    ContactMessage,
)

from .newsletter import send_product_newsletter


# ==========================================
# PRODUCT GALLERY INLINE
# ==========================================

class ProductImageInline(admin.TabularInline):

    model = ProductImage

    extra = 1


# ==========================================
# NEWSLETTER ACTION
# ==========================================

@admin.action(description="Notify Newsletter Subscribers")
def notify_subscribers(modeladmin, request, queryset):

    domain = "https://oshari.onrender.com"

    for product in queryset:
        send_product_newsletter(product, domain)

    modeladmin.message_user(
        request,
        "Newsletter sent successfully."
    )


# ==========================================
# PRODUCTS
# ==========================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "stock",
        "is_available",
        "is_new_drop",
        "notify_subscribers",
    )

    list_editable = (
        "stock",
        "is_available",
        "is_new_drop",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    search_fields = (
        "name",
    )

    inlines = [
        ProductImageInline,
    ]

    def save_model(self, request, obj, form, change):

        send_newsletter = obj.notify_subscribers

        super().save_model(
            request,
            obj,
            form,
            change,
        )

        if send_newsletter:

            domain = "https://oshari.onrender.com"

            send_product_newsletter(
                obj,
                domain,
            )

            obj.notify_subscribers = False

            obj.save(update_fields=["notify_subscribers"])

# ==========================================
# ORDER ITEMS INLINE
# ==========================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "product",
        "quantity",
        "price",
    )

    can_delete = False


# ==========================================
# ORDERS
# ==========================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "full_name",
        "total",
        "status",
        "paid",
        "created_at",
    )

    list_filter = (
        "status",
        "paid",
    )

    search_fields = (
        "order_number",
        "full_name",
        "email",
    )

    inlines = [
        OrderItemInline,
    ]


# ==========================================
# NEWSLETTER
# ==========================================

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


# ==========================================
# CONTACT MESSAGES
# ==========================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
    )

    list_filter = (
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )