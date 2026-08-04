import resend

from django.conf import settings


resend.api_key = settings.RESEND_API_KEY


# ==========================================
# CUSTOMER EMAIL
# ==========================================

def send_order_confirmation(order):

    try:

        items = ""

        for item in order.items.all():

            items += f"""
            <li>
                {item.product.name}
                × {item.quantity}
                — ₦{item.subtotal():,.0f}
            </li>
            """

        resend.Emails.send({

            "from": settings.RESEND_FROM_EMAIL,

            "to": order.email,

            "subject": f"Order Confirmation - {order.order_number}",

            "html": f"""

            <div style="
                font-family:Arial,sans-serif;
                max-width:600px;
                margin:auto;
                padding:40px;
                background:#ffffff;
                border-radius:10px;
            ">

                <h1 style="color:#111111;">

                    Thank you for shopping with
                    OSHARI ITNS

                </h1>

                <p>

                    Your payment has been received successfully.

                </p>

                <hr>

                <h3>

                    Order Number

                </h3>

                <strong>

                    {order.order_number}

                </strong>

                <h3>

                    Items Purchased

                </h3>

                <ul>

                    {items}

                </ul>

                <h3>

                    Total Paid

                </h3>

                <strong>

                    ₦{order.total:,.0f}

                </strong>

                <br><br>

                <p>

                    We'll notify you as soon as your order is shipped.

                </p>

                <br>

                <strong>

                    OSHARI ITNS

                </strong>

            </div>

            """

        })

    except Exception as e:

        print(f"Customer email failed: {e}")


# ==========================================
# ADMIN EMAIL
# ==========================================

def send_admin_notification(order):

    try:

        resend.Emails.send({

            "from": settings.RESEND_FROM_EMAIL,

            "to": settings.ADMIN_ORDER_EMAIL,

            "subject": f"New Paid Order {order.order_number}",

            "html": f"""

            <div style="
                font-family:Arial,sans-serif;
                max-width:600px;
                margin:auto;
                padding:40px;
            ">

                <h2>

                    New Paid Order

                </h2>

                <hr>

                <p>

                    <strong>Order:</strong>

                    {order.order_number}

                </p>

                <p>

                    <strong>Customer:</strong>

                    {order.full_name}

                </p>

                <p>

                    <strong>Email:</strong>

                    {order.email}

                </p>

                <p>

                    <strong>Phone:</strong>

                    {order.phone}

                </p>

                <p>

                    <strong>Address:</strong>

                    {order.address}

                </p>

                <p>

                    <strong>State:</strong>

                    {order.state}

                </p>

                <p>

                    <strong>City:</strong>

                    {order.city}

                </p>

                <p>

                    <strong>Total:</strong>

                    ₦{order.total:,.0f}

                </p>

            </div>

            """

        })

    except Exception as e:

        print(f"Admin email failed: {e}")