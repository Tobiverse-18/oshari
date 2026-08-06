document.addEventListener("DOMContentLoaded", () => {

    // Sidebar
    const menu = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");

    if(menu && sidebar){

        menu.addEventListener("click", ()=>{

            sidebar.classList.toggle("show");

        });
    }
});


document.addEventListener("DOMContentLoaded", () => {

    const message = document.querySelector(".message");

    if(message){

        setTimeout(()=>{

            message.style.opacity = "0";

            message.style.transform = "translateY(-15px)";

            setTimeout(()=>{

                message.remove();

            },300);

        },4000);

    }

});