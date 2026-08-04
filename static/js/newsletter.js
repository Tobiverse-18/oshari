document.addEventListener("DOMContentLoaded", () => {

    const forms = document.querySelectorAll(".newsletter-form");

    forms.forEach(form => {

        const input = form.querySelector("input");

        const button = form.querySelector("button");

        const message = form.querySelector(".newsletter-message");

        const csrf = document.querySelector("[name=csrfmiddlewaretoken]").value;

        form.addEventListener("submit", async function(e){

            e.preventDefault();

            button.disabled = true;

            button.textContent = "Subscribing...";

            if(message){

                message.textContent = "";

                message.className = "newsletter-message";

            }

            const response = await fetch("/newsletter/subscribe/",{

                method:"POST",

                headers:{

                    "X-CSRFToken": csrf,

                },

                body:new FormData(form)

            });

            const data = await response.json();

            if(message){

                if(data.success){

                    message.classList.add("success");

                    input.value = "";

                }else{

                    message.classList.add("error");

                }

                message.textContent = data.message;

            }

            button.disabled = false;

            button.textContent = "Subscribe";

            if(message){

                setTimeout(()=>{

                    message.textContent="";

                    message.className="newsletter-message";

                },5000);

            }

        });

    });

});