from django import forms

from .models import NewsletterSubscriber

from .models import Order

from .models import ContactMessage


class NewsletterForm(forms.ModelForm):

    class Meta:

        model = NewsletterSubscriber

        fields = ["email"]

        widgets = {

            "email": forms.EmailInput(

                attrs={

                    "placeholder": "Enter your email address",

                    "class": "newsletter-input"

                }

            )

        }



class CheckoutForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = [

            "full_name",

            "email",

            "phone",

            "state",

            "city",

            "address",

        ]

        widgets = {

            "full_name": forms.TextInput(attrs={

                "placeholder": "Full Name"

            }),

            "email": forms.EmailInput(attrs={

                "placeholder": "Email Address"

            }),

            "phone": forms.TextInput(attrs={

                "placeholder": "Phone Number"

            }),

            "state": forms.TextInput(attrs={

                "placeholder": "State"

            }),

            "city": forms.TextInput(attrs={

                "placeholder": "City"

            }),

            "address": forms.Textarea(attrs={

                "placeholder": "Delivery Address",

                "rows": 4

            }),

        }


class ContactForm(forms.ModelForm):

    class Meta:

        model = ContactMessage

        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]

        widgets = {

            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "example@email.com",
            }),

            "subject": forms.TextInput(attrs={
                "placeholder": "What is this about?",
            }),

            "message": forms.Textarea(attrs={
                "placeholder": "Write your message...",
                "rows": 6,
            }),

        }