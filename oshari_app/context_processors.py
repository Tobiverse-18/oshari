from .forms import NewsletterForm

from .models import (
    Order,
    ContactMessage,
    NewsletterSubscriber,
)


def newsletter_form(request):

    return {

        "newsletter_form": NewsletterForm()

    }

def dashboard_notifications(request):

    if not request.user.is_authenticated:

        return {}

    new_orders = Order.objects.filter(
        is_read=False
    ).count()

    new_messages = ContactMessage.objects.filter(
        is_read=False
    ).count()

    new_subscribers = NewsletterSubscriber.objects.filter(
        is_read=False
    ).count()

    notification_count = (

        new_orders +

        new_messages +

        new_subscribers

    )

    return {

        "notification_count": notification_count,

        "new_orders": new_orders,

        "new_messages": new_messages,

        "new_subscribers": new_subscribers,

    }