document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("newsletterPopup");

    if (!popup) {
        return;
    }

    const form = document.getElementById("newsletterPopupForm");
    const emailInput = document.getElementById("newsletterPopupEmail");
    const message = document.getElementById("newsletterPopupMessage");
    const closeButton = document.getElementById("newsletterClose");
    const dontRemindCheckbox = document.getElementById("newsletterDontRemind");

    const DONT_REMIND_KEY = "oshari_newsletter_dont_remind";

    function openPopup() {
        if (localStorage.getItem(DONT_REMIND_KEY) === "true") {
            return;
        }

        popup.classList.add("show");
        document.body.style.overflow = "hidden";
    }

    function closePopup() {
        popup.classList.remove("show");
        document.body.style.overflow = "";
    }

    // Close button
    closeButton?.addEventListener("click", closePopup);

    // Click outside the popup
    popup.addEventListener("click", (event) => {
        if (event.target === popup) {
            closePopup();
        }
    });

    // Don't remind me again
    dontRemindCheckbox?.addEventListener("change", () => {
        if (dontRemindCheckbox.checked) {
            localStorage.setItem(DONT_REMIND_KEY, "true");
            closePopup();
        }
    });

    // Newsletter submission
    form?.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const submitButton = form.querySelector(".newsletter-popup-submit");
        const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]")?.value;

        if (!email) {
            message.textContent = "Please enter your email.";
            message.className = "newsletter-popup-message error";
            return;
        }

        if (!csrfToken) {
            message.textContent = "Security token missing. Please refresh the page.";
            message.className = "newsletter-popup-message error";
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Subscribing...";

        try {
            const response = await fetch("/newsletter/subscribe/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    email: email,
                }),
            });

            const data = await response.json();

            if (data.success) {
                message.textContent = data.message || "Thanks for subscribing!";
                message.className = "newsletter-popup-message success";

                localStorage.setItem(DONT_REMIND_KEY, "true");
                form.reset();

                setTimeout(() => {
                    closePopup();
                }, 1800);

                return;
            }

            message.textContent = data.message || "You're already subscribed.";
            message.className = "newsletter-popup-message error";

        } catch (error) {
            console.error("Newsletter error:", error);

            message.textContent =
                "Something went wrong. Please try again later.";

            message.className = "newsletter-popup-message error";

        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Subscribe";
        }
    });

    // Show after 2 seconds
    setTimeout(() => {
        openPopup();
    }, 2000);
});