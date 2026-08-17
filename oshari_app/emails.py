import resend

from django.conf import settings
from django.utils.html import escape

from .models import NewsletterSubscriber


resend.api_key = settings.RESEND_API_KEY


# ==========================================
# OSHARI BRANDING
# ==========================================

LOGO_URL = "https://oshari.com.ng/static/images/logo.png"
SITE_URL = "https://oshari.com.ng"


# ==========================================
# CUSTOMER ORDER CONFIRMATION
# ==========================================

def send_order_confirmation(order):

    try:

        items_html = ""

        for item in order.items.all():

            product_name = escape(item.product.name)
            quantity = item.quantity
            price = item.price
            subtotal = item.subtotal()

            items_html += f"""
            <tr>
                <td style="
                    padding:16px 0;
                    border-bottom:1px solid #eeeeee;
                    color:#222222;
                    font-size:14px;
                ">
                    <strong>{product_name}</strong>
                </td>

                <td style="
                    padding:16px 8px;
                    border-bottom:1px solid #eeeeee;
                    text-align:center;
                    color:#555555;
                    font-size:14px;
                ">
                    {quantity}
                </td>

                <td style="
                    padding:16px 0;
                    border-bottom:1px solid #eeeeee;
                    text-align:right;
                    color:#222222;
                    font-size:14px;
                ">
                    ₦{price:,.0f}
                </td>

                <td style="
                    padding:16px 0;
                    border-bottom:1px solid #eeeeee;
                    text-align:right;
                    color:#222222;
                    font-size:14px;
                ">
                    ₦{subtotal:,.0f}
                </td>
            </tr>
            """

        customer_name = escape(order.full_name)

        resend.Emails.send({

            "from": f"OSHARI ITNS <{settings.RESEND_FROM_EMAIL}>",

            "to": [order.email],

            "subject": f"Order Confirmed — {order.order_number}",

            "html": f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Order Confirmed</title>

</head>

<body style="
margin:0;
padding:0;
background:#f5f5f5;
font-family:Arial,Helvetica,sans-serif;
color:#111111;
">

<table
width="100%"
cellpadding="0"
cellspacing="0"
border="0"
style="background:#f5f5f5;"
>

<tr>

<td align="center" style="padding:30px 15px;">

<table
width="100%"
cellpadding="0"
cellspacing="0"
border="0"
style="
max-width:620px;
background:#ffffff;
border-radius:12px;
overflow:hidden;
"
>

<tr>

<td
align="center"
style="
padding:30px;
border-bottom:1px solid #eeeeee;
"
>

<a
href="{SITE_URL}"
style="text-decoration:none;"
>

<img
src="{LOGO_URL}"
alt="OSHARI ITNS"
style="
display:block;
max-width:170px;
max-height:70px;
width:auto;
height:auto;
margin:auto;
"
>

</a>

</td>

</tr>


<tr>

<td style="padding:40px 35px;">

<div style="
width:52px;
height:52px;
line-height:52px;
border-radius:50%;
background:#111111;
color:#ffffff;
text-align:center;
font-size:24px;
margin-bottom:22px;
">

✓

</div>


<h1 style="
margin:0 0 12px;
font-size:28px;
line-height:1.2;
color:#111111;
">

Order Confirmed

</h1>


<p style="
margin:0 0 8px;
font-size:16px;
line-height:1.6;
color:#444444;
">

Hi {customer_name},

</p>


<p style="
margin:0 0 30px;
font-size:15px;
line-height:1.7;
color:#555555;
">

Thank you for shopping with <strong>OSHARI ITNS</strong>.

Your payment has been received successfully and your order is now being processed.

</p>


<table
width="100%"
cellpadding="0"
cellspacing="0"
border="0"
style="
background:#f7f7f7;
border-radius:8px;
margin-bottom:30px;
"
>

<tr>

<td style="padding:18px;">

<span style="
display:block;
font-size:12px;
color:#777777;
margin-bottom:5px;
">

ORDER NUMBER

</span>

<strong style="
font-size:16px;
color:#111111;
">

{order.order_number}

</strong>

</td>


<td style="
padding:18px;
text-align:right;
">

<span style="
display:block;
font-size:12px;
color:#777777;
margin-bottom:5px;
">

PAYMENT STATUS

</span>

<strong style="
font-size:14px;
color:#16803c;
">

PAID ✓

</strong>

</td>

</tr>

</table>


<h2 style="
margin:0 0 15px;
font-size:18px;
color:#111111;
">

Order Summary

</h2>


<table
width="100%"
cellpadding="0"
cellspacing="0"
border="0"
>

<tr>

<th style="
padding:10px 0;
text-align:left;
border-bottom:2px solid #111111;
font-size:12px;
">

PRODUCT

</th>


<th style="
padding:10px 8px;
text-align:center;
border-bottom:2px solid #111111;
font-size:12px;
">

QTY

</th>


<th style="
padding:10px 0;
text-align:right;
border-bottom:2px solid #111111;
font-size:12px;
">

PRICE

</th>


<th style="
padding:10px 0;
text-align:right;
border-bottom:2px solid #111111;
font-size:12px;
">

TOTAL

</th>

</tr>


{items_html}


<tr>

<td
colspan="3"
style="
padding:22px 0 5px;
text-align:right;
font-size:15px;
color:#555555;
"
>

Total Paid

</td>


<td style="
padding:22px 0 5px;
text-align:right;
font-size:20px;
font-weight:bold;
color:#111111;
">

₦{order.total:,.0f}

</td>

</tr>

</table>


<div style="
margin-top:35px;
padding-top:25px;
border-top:1px solid #eeeeee;
">

<h2 style="
margin:0 0 12px;
font-size:18px;
">

Delivery Information

</h2>

<p style="
margin:0;
font-size:14px;
line-height:1.7;
color:#555555;
">

<strong>{customer_name}</strong><br>

{escape(order.address)}<br>

{escape(order.city)}, {escape(order.state)}<br>

Phone: {escape(order.phone)}

</p>

</div>


<div style="
text-align:center;
margin-top:35px;
">

<a
href="{SITE_URL}/track-order/?order={order.order_number}"
style="
display:inline-block;
padding:14px 28px;
background:#111111;
color:#ffffff;
text-decoration:none;
border-radius:6px;
font-size:14px;
font-weight:bold;
"
>

Track Your Order

</a>

</div>


<p style="
margin:35px 0 0;
text-align:center;
font-size:14px;
line-height:1.7;
color:#666666;
">

We'll notify you as soon as your order ships.

</p>


</td>

</tr>


<tr>

<td
align="center"
style="
padding:25px 30px;
background:#111111;
"
>

<p style="
margin:0 0 8px;
color:#ffffff;
font-size:15px;
font-weight:bold;
">

OSHARI ITNS

</p>


<p style="
margin:0;
color:#aaaaaa;
font-size:12px;
line-height:1.6;
">

Urban Fashion · Luxury Streetwear

</p>


<p style="
margin:12px 0 0;
color:#777777;
font-size:11px;
">

© OSHARI ITNS. All rights reserved.

</p>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""

        })

    except Exception as e:

        print(f"Customer email failed: {e}")


# ==========================================
# ADMIN ORDER NOTIFICATION
# ==========================================

def send_admin_notification(order):

    try:

        items_html = ""

        for item in order.items.all():

            items_html += f"""
            <tr>

                <td style="
                    padding:12px;
                    border-bottom:1px solid #eeeeee;
                ">
                    {escape(item.product.name)}
                </td>

                <td style="
                    padding:12px;
                    text-align:center;
                    border-bottom:1px solid #eeeeee;
                ">
                    {item.quantity}
                </td>

                <td style="
                    padding:12px;
                    text-align:right;
                    border-bottom:1px solid #eeeeee;
                ">
                    ₦{item.subtotal():,.0f}
                </td>

            </tr>
            """

        resend.Emails.send({

            "from": f"OSHARI ITNS <{settings.RESEND_FROM_EMAIL}>",

            "to": [settings.ADMIN_ORDER_EMAIL],

            "subject": f"🛍️ New Paid Order — {order.order_number}",

            "html": f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>New Oshari Order</title>

</head>


<body style="
margin:0;
padding:30px 15px;
background:#f5f5f5;
font-family:Arial,Helvetica,sans-serif;
">

<div style="
max-width:620px;
margin:auto;
background:#ffffff;
border-radius:12px;
overflow:hidden;
">


<div style="
background:#111111;
padding:25px;
text-align:center;
">

<img
src="{LOGO_URL}"
alt="OSHARI ITNS"
style="
max-width:150px;
max-height:60px;
"
>

</div>


<div style="padding:35px;">

<h1 style="
margin:0 0 10px;
font-size:25px;
">

New Paid Order 🛍️

</h1>


<p style="
margin:0 0 25px;
color:#666666;
">

A customer has successfully completed payment.

</p>


<div style="
padding:18px;
background:#f7f7f7;
border-radius:8px;
margin-bottom:25px;
">

<p style="margin:0 0 8px;">

<strong>Order:</strong>
{order.order_number}

</p>


<p style="margin:0;">

<strong>Status:</strong>

<span style="color:#16803c;">

PAID ✓

</span>

</p>

</div>


<h2 style="font-size:18px;">

Customer Information

</h2>


<p style="
line-height:1.8;
color:#444444;
">

<strong>Name:</strong>
{escape(order.full_name)}
<br>

<strong>Email:</strong>
{escape(order.email)}
<br>

<strong>Phone:</strong>
{escape(order.phone)}
<br>

<strong>Address:</strong>
{escape(order.address)}
<br>

<strong>City:</strong>
{escape(order.city)}
<br>

<strong>State:</strong>
{escape(order.state)}

</p>


<h2 style="
margin-top:30px;
font-size:18px;
">

Items

</h2>


<table
width="100%"
cellpadding="0"
cellspacing="0"
border="0"
>

<tr>

<th style="
padding:12px;
text-align:left;
border-bottom:2px solid #111111;
">

Product

</th>


<th style="
padding:12px;
text-align:center;
border-bottom:2px solid #111111;
">

Qty

</th>


<th style="
padding:12px;
text-align:right;
border-bottom:2px solid #111111;
">

Total

</th>

</tr>


{items_html}


<tr>

<td
colspan="2"
style="
padding:20px 12px;
text-align:right;
font-weight:bold;
">

TOTAL PAID

</td>


<td style="
padding:20px 12px;
text-align:right;
font-size:18px;
font-weight:bold;
">

₦{order.total:,.0f}

</td>

</tr>

</table>


<div style="
text-align:center;
margin-top:30px;
">

<a
href="{SITE_URL}/dashboard/orders/{order.id}/"
style="
display:inline-block;
padding:14px 25px;
background:#111111;
color:#ffffff;
text-decoration:none;
border-radius:6px;
font-weight:bold;
"
>

View Order in Dashboard

</a>

</div>


</div>


<div style="
padding:20px;
background:#111111;
text-align:center;
color:#888888;
font-size:11px;
">

OSHARI ITNS · Internal Order Notification

</div>


</div>

</body>

</html>
"""

        })

    except Exception as e:

        print(f"Admin email failed: {e}")


# ==========================================
# CONTACT FORM NOTIFICATION
# ==========================================

def send_contact_notification(contact):

    try:

        resend.Emails.send({

            "from": f"OSHARI ITNS <{settings.RESEND_FROM_EMAIL}>",

            "to": [settings.ADMIN_ORDER_EMAIL],

            "subject": f"New Contact Message — {contact.subject}",

            "html": f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>New Contact Message</title>

</head>


<body style="
margin:0;
padding:30px 15px;
background:#f5f5f5;
font-family:Arial,Helvetica,sans-serif;
">

<div style="
max-width:620px;
margin:auto;
background:#ffffff;
border-radius:12px;
overflow:hidden;
">


<div style="
background:#111111;
padding:25px;
text-align:center;
">

<img
src="{LOGO_URL}"
alt="OSHARI ITNS"
style="
max-width:150px;
max-height:60px;
"
>

</div>


<div style="padding:35px;">

<h1 style="
margin:0 0 10px;
font-size:25px;
">

New Contact Message

</h1>


<p style="
margin:0 0 25px;
color:#666666;
">

Someone has submitted a message through the Oshari website.

</p>


<div style="
background:#f7f7f7;
padding:20px;
border-radius:8px;
margin-bottom:25px;
">

<p style="margin:0 0 8px;">

<strong>Name:</strong>

{escape(contact.name)}

</p>


<p style="margin:0 0 8px;">

<strong>Email:</strong>

{escape(contact.email)}

</p>


<p style="margin:0;">

<strong>Subject:</strong>

{escape(contact.subject)}

</p>

</div>


<h2 style="font-size:18px;">

Message

</h2>


<div style="
background:#f7f7f7;
padding:20px;
border-radius:8px;
line-height:1.7;
color:#444444;
white-space:pre-line;
">

{escape(contact.message)}

</div>


<div style="
text-align:center;
margin-top:30px;
">

<a
href="{SITE_URL}/dashboard/contacts/view/{contact.id}/"
style="
display:inline-block;
padding:14px 25px;
background:#111111;
color:#ffffff;
text-decoration:none;
border-radius:6px;
font-weight:bold;
"
>

View Message in Dashboard

</a>

</div>


</div>


<div style="
padding:20px;
background:#111111;
text-align:center;
color:#888888;
font-size:11px;
">

OSHARI ITNS · Contact Notification

</div>


</div>

</body>

</html>
"""

        })

    except Exception as e:

        print(f"Contact email failed: {e}")


# ==========================================
# NEW PRODUCT NEWSLETTER NOTIFICATION
# ==========================================

def send_new_product_notification(product):

    try:

        # Get every newsletter subscriber.
        # is_read is NOT used here because it is unrelated
        # to whether someone is subscribed.

        subscriber_emails = list(
            NewsletterSubscriber.objects
            .values_list("email", flat=True)
        )


        if not subscriber_emails:

            print("No newsletter subscribers found.")

            return


        product_name = escape(product.name)

        product_description = escape(
            product.description
        )

        product_url = (
            f"{SITE_URL}/product/{product.pk}/"
        )


        # ==========================================
        # PRODUCT IMAGE
        # ==========================================

        image_html = ""

        if product.image:

            image_url = product.image.url

            if image_url.startswith("/"):

                image_url = (
                    f"{SITE_URL}{image_url}"
                )

            image_html = f"""
            <img
                src="{image_url}"
                alt="{product_name}"
                style="
                    display:block;
                    width:100%;
                    max-height:520px;
                    object-fit:cover;
                "
            >
            """


        # ==========================================
        # NEWSLETTER HTML
        # ==========================================

        html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>New Drop — OSHARI ITNS</title>

</head>


<body style="
margin:0;
padding:30px 15px;
background:#f5f5f5;
font-family:Arial,Helvetica,sans-serif;
color:#111111;
">


<div style="
max-width:620px;
margin:auto;
background:#ffffff;
border-radius:12px;
overflow:hidden;
">


<!-- HEADER -->

<div style="
background:#111111;
padding:28px;
text-align:center;
">

<a
href="{SITE_URL}"
style="text-decoration:none;"
>

<img
src="{LOGO_URL}"
alt="OSHARI ITNS"
style="
max-width:160px;
max-height:65px;
"
>

</a>

</div>


<!-- PRODUCT IMAGE -->

{image_html}


<!-- CONTENT -->

<div style="padding:35px;">

<p style="
margin:0 0 10px;
font-size:12px;
font-weight:bold;
letter-spacing:2px;
color:#777777;
">

NEW DROP

</p>


<h1 style="
margin:0 0 15px;
font-size:30px;
line-height:1.2;
">

{product_name}

</h1>


<p style="
margin:0 0 20px;
font-size:22px;
font-weight:bold;
">

₦{product.price:,.0f}

</p>


<p style="
margin:0 0 30px;
font-size:15px;
line-height:1.8;
color:#555555;
">

{product_description}

</p>


<div style="text-align:center;">

<a
href="{product_url}"
style="
display:inline-block;
padding:15px 32px;
background:#111111;
color:#ffffff;
text-decoration:none;
border-radius:6px;
font-size:14px;
font-weight:bold;
"
>

SHOP THIS DROP

</a>

</div>


<p style="
margin:35px 0 0;
text-align:center;
font-size:13px;
line-height:1.7;
color:#777777;
">

You're receiving this email because you subscribed
to the OSHARI ITNS newsletter.

</p>

</div>


<!-- FOOTER -->

<div style="
padding:25px;
background:#111111;
text-align:center;
">

<p style="
margin:0 0 8px;
color:#ffffff;
font-size:15px;
font-weight:bold;
">

OSHARI ITNS

</p>


<p style="
margin:0;
color:#aaaaaa;
font-size:12px;
">

Urban Fashion · Luxury Streetwear

</p>


<p style="
margin:12px 0 0;
color:#777777;
font-size:11px;
">

© OSHARI ITNS. All rights reserved.

</p>

</div>


</div>

</body>

</html>
"""


        # ==========================================
        # SEND EMAIL TO EACH SUBSCRIBER
        # ==========================================

        sent_count = 0

        for email in subscriber_emails:

            try:

                resend.Emails.send({

                    "from": (
                        f"OSHARI ITNS "
                        f"<{settings.RESEND_FROM_EMAIL}>"
                    ),

                    "to": [email],

                    "subject": (
                        f"🔥 New Drop — "
                        f"{product.name}"
                    ),

                    "html": html,

                })

                sent_count += 1

            except Exception as subscriber_error:

                print(
                    f"Newsletter failed for {email}: "
                    f"{subscriber_error}"
                )


        print(
            f"New product newsletter sent: "
            f"{sent_count}/{len(subscriber_emails)}"
        )


    except Exception as e:

        print(
            f"Newsletter email failed: {e}"
        )
