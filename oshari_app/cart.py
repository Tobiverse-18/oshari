from .models import Product


class Cart:

    def __init__(self, request):

        self.session = request.session

        self.cart = self.session.get("cart")

        if self.cart is None:

            self.cart = {}

            self.session["cart"] = self.cart


    # ==========================================
    # ADD PRODUCT
    # ==========================================

    def add(self, product, quantity=1, size=None):

        product_id = str(product.id)

        quantity = int(quantity)

        # Create a unique cart item based on
        # product + size

        cart_key = f"{product_id}_{size or 'no-size'}"


        if cart_key not in self.cart:

            self.cart[cart_key] = {

                "product_id": product_id,

                "quantity": quantity,

                "size": size,

            }

        else:

            self.cart[cart_key]["quantity"] += quantity


        self.save()


    # ==========================================
    # UPDATE
    # ==========================================

    def update(self, product, quantity, size=None):

        product_id = str(product.id)

        quantity = int(quantity)

        cart_key = f"{product_id}_{size or 'no-size'}"


        if cart_key in self.cart:

            self.cart[cart_key]["quantity"] = quantity

            self.save()


    # ==========================================
    # REMOVE
    # ==========================================

    def remove(self, product, size=None):

        product_id = str(product.id)

        cart_key = f"{product_id}_{size or 'no-size'}"


        if cart_key in self.cart:

            del self.cart[cart_key]

            self.save()


    # ==========================================
    # CLEAR
    # ==========================================

    def clear(self):

        self.cart = {}

        self.session["cart"] = self.cart

        self.session.modified = True


    # ==========================================
    # SAVE
    # ==========================================

    def save(self):

        self.session["cart"] = self.cart

        self.session.modified = True


    # ==========================================
    # ITERATE CART
    # ==========================================

    def __iter__(self):

        product_ids = [

            item["product_id"]

            for item in self.cart.values()

        ]


        products = Product.objects.filter(

            id__in=product_ids

        )


        products_by_id = {

            str(product.id): product

            for product in products

        }


        for cart_item in self.cart.values():

            product_id = cart_item["product_id"]

            product = products_by_id.get(product_id)


            if not product:

                continue


            item = cart_item.copy()

            item["product"] = product

            item["total_price"] = (

                product.price *

                item["quantity"]

            )


            yield item


    # ==========================================
    # TOTAL ITEMS
    # ==========================================

    def __len__(self):

        return self.get_total_items()


    def get_total_items(self):

        return sum(

            item["quantity"]

            for item in self.cart.values()

        )


    def get_total_quantity(self):

        return self.get_total_items()


    # ==========================================
    # TOTAL PRICE
    # ==========================================

    def get_total_price(self):

        total = 0

        for item in self:

            total += item["total_price"]


        return total