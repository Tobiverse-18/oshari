from django.db import models


# ==========================================
# PRODUCTS
# ==========================================

class Product(models.Model):

    name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    track_stock = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to="products/"
    )

    description = models.TextField()

    is_new_drop = models.BooleanField(default=True)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    notify_subscribers = models.BooleanField(
        default=False,
        verbose_name="Notify Newsletter Subscribers"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


# ==========================================
# PRODUCT GALLERY
# ==========================================

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    image = models.ImageField(
        upload_to="products/gallery/"
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.product.name} Gallery Image"


# ==========================================
# NEWSLETTER
# ==========================================

class NewsletterSubscriber(models.Model):

    email = models.EmailField(unique=True)

    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# ==========================================
# ORDERS
# ==========================================

class Order(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    order_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )

    full_name = models.CharField(max_length=200)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    state = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    address = models.TextField()

    total = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_number} - {self.full_name}"


# ==========================================
# ORDER ITEMS
# ==========================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"


# ==========================================
# CONTACT MESSAGES
# ==========================================

class ContactMessage(models.Model):

    name = models.CharField(max_length=150)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"