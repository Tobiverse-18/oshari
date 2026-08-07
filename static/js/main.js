document.addEventListener("DOMContentLoaded", () => {

    lucide.createIcons();

});

function showToast(message, type = "success") {

    const toast = document.getElementById("toast");

    if (!toast) return;

    const title = document.getElementById("toast-title");
    const product = document.getElementById("toast-product");
    const quantity = document.getElementById("toast-quantity");

    title.textContent =
        type === "success"
        ? "Success"
        : type === "error"
        ? "Error"
        : "Notice";

    product.textContent = message;

    quantity.textContent = "";

    toast.classList.remove(
        "success",
        "error",
        "info",
        "show"
    );

    toast.classList.add(type);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

    }, 4000);

}