document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".newsletter-form");

    if(!form) return;

    const input = form.querySelector("input");

    const button = form.querySelector("button");

    const message = document.querySelector(".newsletter-message");

    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

    form.addEventListener("submit", async function(e){

        e.preventDefault();

        button.disabled = true;

        button.textContent = "Subscribing...";

        message.textContent = "";

        message.className = "newsletter-message";

        const response = await fetch("/newsletter/subscribe/",{

            method:"POST",

            headers:{
                "X-CSRFToken":csrf,
            },

            body:new FormData(form)

        });

        const data = await response.json();

        if(data.success){

            message.classList.add("success");

            input.value = "";

        }

        else{

            message.classList.add("error");

        }

        message.textContent = data.message;

        button.disabled = false;

        button.textContent = "Subscribe";

        setTimeout(()=>{

            message.textContent="";

            message.className="newsletter-message";

        },5000);

    });

});