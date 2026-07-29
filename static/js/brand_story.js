document.addEventListener("DOMContentLoaded", () => {

    function slider(selector){

        const track = document.querySelector(selector);

        if(!track) return;

        let current = 0;

        const totalSlides = track.children.length;

        setInterval(() => {

            current = (current + 1) % totalSlides;

            track.style.transform = `translateX(-${current * (100 / totalSlides)}%)`;

        },3000);

    }

    slider(".story-track");
    slider(".mobile-track");

});