from .models import Product


class Cart:

    def __init__(self, request):

        self.session = request.session

        self.cart = self.session.get("cart")

        if self.cart is None:

            self.cart = {}

            self.session["cart"] = self.cart

    def add(self, product, quantity=1):

        product_id = str(product.id)

        quantity = int(quantity)

        if product_id not in self.cart:

            self.cart[product_id] = {
                "quantity": quantity
            }

        else:

            self.cart[product_id]["quantity"] += quantity

        self.save()

    def update(self, product, quantity):

        product_id = str(product.id)

        quantity = int(quantity)

        if product_id in self.cart:

            self.cart[product_id]["quantity"] = quantity

            self.save()

    def remove(self, product):

        product_id = str(product.id)

        if product_id in self.cart:

            del self.cart[product_id]

            self.save()

    def clear(self):

        self.cart = {}

        self.session["cart"] = self.cart

        self.session.modified = True

    def save(self):

        self.session["cart"] = self.cart

        self.session.modified = True

    def __iter__(self):

        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        for product in products:

            item = self.cart[str(product.id)].copy()

            item["product"] = product

            item["total_price"] = (
                product.price * item["quantity"]
            )

            yield item

    def __len__(self):

        return sum(

            item["quantity"]

            for item in self.cart.values()

        )

    def get_total_items(self):

        return sum(

            item["quantity"]

            for item in self.cart.values()

        )

    def get_total_quantity(self):

        return self.get_total_items()

    def get_total_price(self):

        total = 0

        for item in self:

            total += item["total_price"]

        return total