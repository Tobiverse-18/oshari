// ==========================================
// OSHARI ITNS THEME SWITCHER
// ==========================================


document.addEventListener("DOMContentLoaded", () => {


    const themeToggle = document.getElementById("theme-toggle");


    // Stop if button doesn't exist

    if (!themeToggle) {
        console.warn("Theme toggle button not found");
        return;
    }


    const icon = themeToggle.querySelector("i");



    // ==========================================
    // LOAD SAVED THEME
    // ==========================================


    const savedTheme = localStorage.getItem("theme");


    if (savedTheme === "dark") {

        document.body.classList.add("dark-theme");

        if(icon){
            icon.setAttribute("data-lucide", "sun");
        }

    }



    // ==========================================
    // THEME BUTTON CLICK
    // ==========================================


    themeToggle.addEventListener("click", () => {


        // Add transition effect

        document.body.classList.add("theme-transition");


        // Toggle dark mode

        document.body.classList.toggle("dark-theme");



        const isDarkMode = document.body.classList.contains("dark-theme");



        // Save preference

        if(isDarkMode){


            localStorage.setItem("theme","dark");


            if(icon){
                icon.setAttribute("data-lucide","sun");
            }


        }else{


            localStorage.setItem("theme","light");


            if(icon){
                icon.setAttribute("data-lucide","moon");
            }

        }



        // Reload lucide icons

        if(window.lucide){

            lucide.createIcons();

        }



        // Remove transition class

        setTimeout(()=>{

            document.body.classList.remove("theme-transition");

        },400);



    });



});