document.addEventListener("DOMContentLoaded", () => {

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    document.querySelectorAll(".quantity-box").forEach(box => {

        const minus = box.querySelector(".qty-btn:first-child");

        const plus = box.querySelector(".qty-btn:last-child");

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
                }),
            })
            .then(response => {
                console.log("Status:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("Response:", data);

                document.querySelector(
                    `[data-subtotal="${id}"]`
                ).textContent = "₦" + Number(data.subtotal).toLocaleString();

                document.getElementById("cart-total").textContent =
                    "₦" + Number(data.total).toLocaleString();
            })
            .catch(error => {
                console.error("AJAX Error:", error);
});

        }

        plus.onclick = ()=>{

            input.value++;

            updateCart();

        }

        minus.onclick = ()=>{

            if(input.value>1){

                input.value--;

                updateCart();

            }

        };

    });

});