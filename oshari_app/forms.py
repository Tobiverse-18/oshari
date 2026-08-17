from django import forms
from .models import NewsletterSubscriber
from .models import Order
from .models import ContactMessage
from .models import ProductSize


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


from django import forms

from .models import Product, ProductSize


class ProductForm(forms.ModelForm):

    available_sizes = forms.MultipleChoiceField(
        choices=ProductSize.SIZE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Available Sizes",
    )

    class Meta:

        model = Product

        fields = [
            "name",
            "slug",
            "price",
            "stock",
            "description",
            "image",
            "is_available",
            "is_new_drop",
            "notify_subscribers",
            "available_sizes",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance.pk:

            self.fields["available_sizes"].initial = (
                self.instance.sizes
                .values_list(
                    "size",
                    flat=True
                )
            )

    def save(self, commit=True):

        product = super().save(
            commit=commit
        )

        if commit:

            selected_sizes = self.cleaned_data.get(
                "available_sizes",
                []
            )

            # Remove sizes that are no longer selected

            product.sizes.exclude(
                size__in=selected_sizes
            ).delete()

            # Add newly selected sizes

            for size in selected_sizes:

                ProductSize.objects.get_or_create(
                    product=product,
                    size=size
                )

        return product