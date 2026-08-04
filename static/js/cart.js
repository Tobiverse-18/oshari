document.addEventListener("DOMContentLoaded", () => {

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // ==========================
    // QUANTITY UPDATE
    // ==========================

    document.querySelectorAll(".quantity-box").forEach(box => {

        const minus = box.querySelector(".minus");
        const plus = box.querySelector(".plus");
        const input = box.querySelector("input");

        const id = box.dataset.id;

        function updateCart() {

            fetch("/cart/update/", {

                method: "POST",

                headers: {

                    "X-CSRFToken": csrf,
                    "Content-Type": "application/x-www-form-urlencoded",

                },

                body: new URLSearchParams({

                    product_id: id,
                    quantity: input.value,

                })

            })

            .then(res => res.json())

            .then(data => {

                document.querySelector(
                    `[data-subtotal="${id}"]`
                ).textContent =
                "₦" + Number(data.subtotal).toLocaleString();

                document.getElementById(
                    "cart-total"
                ).textContent =
                "₦" + Number(data.total).toLocaleString();

                const badge = document.getElementById(
                    "floating-cart-count"
                );

                if (badge) {

                    badge.textContent = data.items;

                }

            });

        }

        plus.addEventListener("click", () => {

            input.value++;

            updateCart();

        });

        minus.addEventListener("click", () => {

            if (parseInt(input.value) > 1) {

                input.value--;

                updateCart();

            }

        });

    });

    // ==========================
    // REMOVE ITEM
    // ==========================

    document.querySelectorAll(".remove").forEach(button => {

        button.addEventListener("click", function () {

            const id = this.dataset.remove;

            fetch(`/cart/remove/${id}/`, {

                method: "POST",

                headers: {

                    "X-CSRFToken": csrf,

                }

            })

            .then(res => res.json())

            .then(data => {

                const item = document.querySelector(

                    `[data-cart-item="${id}"]`

                );

                if (item) {

                    item.remove();

                }

                document.getElementById(

                    "cart-total"

                ).textContent =
                "₦" + Number(data.total).toLocaleString();

                const badge = document.getElementById(

                    "floating-cart-count"

                );

                if (badge) {

                    badge.textContent = data.items;

                }

                if (data.empty) {

                    location.reload();

                }

            });

        });

    });

});