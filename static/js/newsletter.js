document.addEventListener("DOMContentLoaded", () => {

    const overlay = document.getElementById("newsletterPopup");

    if (!overlay) {
        return;
    }

    const form = document.getElementById("newsletterPopupForm");
    const emailInput = document.getElementById("newsletterPopupEmail");
    const message = document.getElementById("newsletterPopupMessage");

    const closeButton = document.getElementById("newsletterClose");
    const dontRemindCheckbox = document.getElementById("newsletterDontRemind");

    const DONT_REMIND_KEY = "oshari_newsletter_dont_remind";


    /* ==========================================
       OPEN POPUP
    ========================================== */

    function openPopup() {

        const dontRemind =
            localStorage.getItem(DONT_REMIND_KEY);

        if (dontRemind === "true") {
            return;
        }

        overlay.classList.add("show");

        document.body.style.overflow = "hidden";
    }


    /* ==========================================
       CLOSE POPUP
    ========================================== */

    function closePopup() {

        overlay.classList.remove("show");

        document.body.style.overflow = "";
    }


    /* ==========================================
       CLOSE BUTTON
    ========================================== */

    if (closeButton) {

        closeButton.addEventListener(
            "click",
            closePopup
        );

    }


    /* ==========================================
       CLICK OUTSIDE POPUP
    ========================================== */

    overlay.addEventListener("click", (event) => {

        if (event.target === overlay) {
            closePopup();
        }

    });


    /* ==========================================
       DON'T REMIND ME AGAIN
    ========================================== */

    if (dontRemindCheckbox) {

        dontRemindCheckbox.addEventListener(
            "change",
            () => {

                if (dontRemindCheckbox.checked) {

                    localStorage.setItem(
                        DONT_REMIND_KEY,
                        "true"
                    );

                    closePopup();

                }

            }
        );

    }


    /* ==========================================
       SUBSCRIBE
    ========================================== */

    if (form) {

        form.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();

                const email =
                    emailInput.value.trim();

                if (!email) {

                    message.textContent =
                        "Please enter your email.";

                    message.className =
                        "newsletter-popup-message error";

                    return;

                }


                const csrfInput =
                    form.querySelector(
                        "[name=csrfmiddlewaretoken]"
                    );

                if (!csrfInput) {

                    message.textContent =
                        "Security token missing. Please refresh the page.";

                    message.className =
                        "newsletter-popup-message error";

                    return;

                }


                const submitButton =
                    form.querySelector(
                        ".newsletter-popup-submit"
                    );

                const originalText =
                    submitButton.textContent;


                submitButton.disabled = true;

                submitButton.textContent =
                    "Subscribing...";


                try {

                    const response =
                        await fetch(
                            "/newsletter/subscribe/",
                            {
                                method: "POST",

                                headers: {
                                    "X-CSRFToken":
                                        csrfInput.value,

                                    "X-Requested-With":
                                        "XMLHttpRequest",

                                    "Content-Type":
                                        "application/x-www-form-urlencoded"
                                },

                                body:
                                    `email=${encodeURIComponent(email)}`
                            }
                        );


                    const data =
                        await response.json();


                    if (data.success) {

                        message.textContent =
                            data.message;

                        message.className =
                            "newsletter-popup-message success";

                        form.reset();

                        localStorage.setItem(
                            DONT_REMIND_KEY,
                            "true"
                        );


                        setTimeout(() => {
                            closePopup();
                        }, 1500);


                    } else {

                        message.textContent =
                            data.message;

                        message.className =
                            "newsletter-popup-message error";

                    }


                } catch (error) {

                    console.error(
                        "Newsletter error:",
                        error
                    );

                    message.textContent =
                        "Something went wrong. Please try again.";

                    message.className =
                        "newsletter-popup-message error";


                } finally {

                    submitButton.disabled = false;

                    submitButton.textContent =
                        originalText;

                }

            }
        );

    }


    /* ==========================================
       SHOW AFTER DELAY
    ========================================== */

    setTimeout(() => {
        openPopup();
    }, 2000);

});