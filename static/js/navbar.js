document.addEventListener("DOMContentLoaded", () => {

    const menuBtn = document.getElementById("menu-btn");

    const closeBtn = document.getElementById("close-menu");

    const mobileMenu = document.getElementById("mobile-menu");

    const overlay = document.getElementById("mobile-overlay");

    const links = document.querySelectorAll(".mobile-nav-links a");

    function openMenu(){

        mobileMenu.classList.add("active");

        overlay.classList.add("active");

        document.body.style.overflow = "hidden";

    }

    function closeMenu(){

        mobileMenu.classList.remove("active");

        overlay.classList.remove("active");

        document.body.style.overflow = "";

    }

    menuBtn.addEventListener("click", openMenu);

    closeBtn.addEventListener("click", closeMenu);

    overlay.addEventListener("click", closeMenu);

    links.forEach(link=>{

        link.addEventListener("click", closeMenu);

    });

});