import resend

from django.conf import settings
from django.template.loader import render_to_string

from .models import NewsletterSubscriber


resend.api_key = settings.RESEND_API_KEY


def send_product_newsletter(product, domain):

    subscribers = NewsletterSubscriber.objects.all()

    if not subscribers.exists():
        return

    html = render_to_string(

        "emails/new_drop.html",

        {
            "product": product,
            "image_url": f"{domain}{product.image.url}",
            "product_url": f"{domain}/product/{product.slug}/",
        },

    )

    for subscriber in subscribers:

        resend.Emails.send({

            "from": settings.RESEND_FROM_EMAIL,

            "to": subscriber.email,

            "subject": f"🔥 New Drop • {product.name}",

            "html": html,

        })