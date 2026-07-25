// ==========================================
// HERO SLIDER
// ==========================================

const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");
const nextBtn = document.querySelector(".next");
const prevBtn = document.querySelector(".prev");

let currentSlide = 0;
let autoSlide;

// ==========================
// Show Slide
// ==========================

function showSlide(index){

    slides.forEach(slide => slide.classList.remove("active"));
    dots.forEach(dot => dot.classList.remove("active"));

    slides[index].classList.add("active");
    dots[index].classList.add("active");

}

// ==========================
// Next Slide
// ==========================

function nextSlide(){

    currentSlide++;

    if(currentSlide >= slides.length){
        currentSlide = 0;
    }

    showSlide(currentSlide);

}

// ==========================
// Previous Slide
// ==========================

function previousSlide(){

    currentSlide--;

    if(currentSlide < 0){
        currentSlide = slides.length - 1;
    }

    showSlide(currentSlide);

}

// ==========================
// Buttons
// ==========================

nextBtn.addEventListener("click", () =>{

    nextSlide();
    resetAutoSlide();

});

prevBtn.addEventListener("click", () =>{

    previousSlide();
    resetAutoSlide();

});

// ==========================
// Dots
// ==========================

dots.forEach((dot,index)=>{

    dot.addEventListener("click",()=>{

        currentSlide = index;
        showSlide(currentSlide);

        resetAutoSlide();

    });

});

// ==========================
// Auto Slide
// ==========================

function startAutoSlide(){

    autoSlide = setInterval(()=>{

        nextSlide();

    },5000);

}

function resetAutoSlide(){

    clearInterval(autoSlide);

    startAutoSlide();

}

startAutoSlide();

// ==========================================
// Mobile Background Slider
// ==========================================

const mobileImages = [
    "/static/images/hero/model-1.jpg",
    "/static/images/hero/model-2.jpg",
    "/static/images/hero/model-3.jpg",
    "/static/images/hero/model-4.jpg",
    "/static/images/hero/model-5.jpg"
];

let mobileIndex = 0;

function mobileHeroSlider(){

    if(window.innerWidth > 768) return;

    mobileIndex++;

    if(mobileIndex >= mobileImages.length){
        mobileIndex = 0;
    }

    document.querySelector(".hero-background").style.backgroundImage =
        `url('${mobileImages[mobileIndex]}')`;

}

setInterval(mobileHeroSlider,5000);