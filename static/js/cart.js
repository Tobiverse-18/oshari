document.addEventListener("DOMContentLoaded", () => {

    const csrfInput = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    );

    if (!csrfInput) {
        console.error("CSRF token not found.");
        return;
    }

    const csrf = csrfInput.value;


    // ==========================================
    // QUANTITY UPDATE
    // ==========================================

    document.querySelectorAll(".quantity-box").forEach(box => {

        const minus = box.querySelector(".minus");
        const plus = box.querySelector(".plus");
        const input = box.querySelector("input");

        const productId = box.dataset.id;
        const size = box.dataset.size || "";


        function updateCart() {

            const quantity =
                parseInt(input.value) || 1;


            fetch("/cart/update/", {

                method: "POST",

                headers: {

                    "X-CSRFToken": csrf,

                    "Content-Type":
                        "application/x-www-form-urlencoded",

                },

                body: new URLSearchParams({

                    product_id: productId,

                    quantity: quantity,

                    size: size,

                })

            })

            .then(response => {

                if (!response.ok) {
                    throw new Error(
                        "Cart update request failed."
                    );
                }

                return response.json();

            })

            .then(data => {

                if (!data.success) {

                    alert(
                        data.message ||
                        "Unable to update cart."
                    );

                    return;

                }


                // ==================================
                // SUBTOTAL
                // ==================================

                const subtotal =
                    document.querySelector(
                        `[data-subtotal="${productId}"][data-size="${CSS.escape(size)}"]`
                    );


                if (subtotal) {

                    subtotal.textContent =
                        "₦" +
                        Number(
                            data.subtotal
                        ).toLocaleString();

                }


                // ==================================
                // CART TOTAL
                // ==================================

                const cartTotal =
                    document.getElementById(
                        "cart-total"
                    );


                if (cartTotal) {

                    cartTotal.textContent =
                        "₦" +
                        Number(
                            data.total
                        ).toLocaleString();

                }


                // ==================================
                // CART BADGE
                // ==================================

                const badge =
                    document.getElementById(
                        "floating-cart-count"
                    );


                if (badge) {

                    badge.textContent =
                        data.items;

                }

            })

            .catch(error => {

                console.error(
                    "Cart update error:",
                    error
                );

            });

        }


        // ==========================================
        // PLUS
        // ==========================================

        if (plus) {

            plus.addEventListener(
                "click",
                () => {

                    let quantity =
                        parseInt(input.value) || 1;

                    quantity++;

                    input.value = quantity;

                    updateCart();

                }
            );

        }


        // ==========================================
        // MINUS
        // ==========================================

        if (minus) {

            minus.addEventListener(
                "click",
                () => {

                    let quantity =
                        parseInt(input.value) || 1;


                    if (quantity > 1) {

                        quantity--;

                        input.value =
                            quantity;

                        updateCart();

                    }

                }
            );

        }

    });


    // ==========================================
    // REMOVE ITEM
    // ==========================================

    document.querySelectorAll(".remove").forEach(
        button => {

            button.addEventListener(
                "click",
                function () {

                    const productId =
                        this.dataset.remove;

                    const size =
                        this.dataset.size || "";


                    fetch(
                        `/cart/remove/${productId}/`,
                        {

                            method: "POST",

                            headers: {

                                "X-CSRFToken":
                                    csrf,

                                "Content-Type":
                                    "application/x-www-form-urlencoded",

                            },

                            body:
                                new URLSearchParams({

                                    size: size,

                                })

                        }
                    )

                    .then(response => response.json())

                    .then(data => {

                        if (!data.success) {

                            alert(
                                data.message ||
                                "Unable to remove item."
                            );

                            return;

                        }


                        const item =
                            document.querySelector(
                                `[data-cart-item="${productId}"][data-size="${CSS.escape(size)}"]`
                            );


                        if (item) {

                            item.remove();

                        }


                        const cartTotal =
                            document.getElementById(
                                "cart-total"
                            );


                        if (cartTotal) {

                            cartTotal.textContent =
                                "₦" +
                                Number(
                                    data.total
                                ).toLocaleString();

                        }


                        const badge =
                            document.getElementById(
                                "floating-cart-count"
                            );


                        if (badge) {

                            badge.textContent =
                                data.items;

                        }


                        if (data.empty) {

                            location.reload();

                        }

                    })

                    .catch(error => {

                        console.error(
                            "Remove cart error:",
                            error
                        );

                    });

                }
            );

        }
    );

});