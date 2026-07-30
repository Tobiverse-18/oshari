document.addEventListener("DOMContentLoaded", () => {

    const minus = document.querySelector(".minus");
    const plus = document.querySelector(".plus");

    const qtyInput = document.getElementById("quantity");
    const hiddenQty = document.getElementById("hidden-quantity");

    if (plus) {

        plus.onclick = () => {

            qtyInput.value++;

            hiddenQty.value = qtyInput.value;

        };

    }

    if (minus) {

        minus.onclick = () => {

            if (qtyInput.value > 1) {

                qtyInput.value--;

                hiddenQty.value = qtyInput.value;

            }

        };

    }

    const form = document.getElementById("add-to-cart-form");

    if (!form) return;

    form.addEventListener("submit", function(e){

        e.preventDefault();

        const formData = new FormData(form);

        fetch(form.action,{

            method:"POST",

            headers:{

                "X-CSRFToken":form.querySelector("[name=csrfmiddlewaretoken]").value

            },

            body:formData

        })

        .then(res=>res.json())

        .then(data=>{

            if(data.success){

                const badge = document.getElementById("floating-cart-count");

                badge.textContent = data.cart_count;

                const cart = document.getElementById("floating-cart");

                cart.classList.add("cart-bounce");

                setTimeout(()=>{

                    cart.classList.remove("cart-bounce");

                },450);

                const toast = document.getElementById("toast");

                document.getElementById("toast-title").textContent =
                "Added to Cart";

                document.getElementById("toast-product").textContent =
                data.product;

                document.getElementById("toast-quantity").textContent =
                `${data.quantity} item${data.quantity > 1 ? "s" : ""} added`;

                toast.classList.add("show");

                setTimeout(()=>{

                    toast.classList.remove("show");

                },3000);

            }

        });

    });

});