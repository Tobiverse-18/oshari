document.addEventListener("DOMContentLoaded", ()=>{

    const main=document.getElementById("product-main-image");

    if(!main) return;

    const prev=document.getElementById("prev-image");

    const next=document.getElementById("next-image");

    const images=[main.src];

    document.querySelectorAll(".gallery-image").forEach(img=>{

        images.push(img.src);

    });

    let current=0;

    function showImage(){

        main.style.opacity="0";

        setTimeout(()=>{

            main.src=images[current];

            main.style.opacity="1";

        },150);

    }

    next.addEventListener("click",()=>{

        current++;

        if(current>=images.length){

            current=0;

        }

        showImage();

    });

    prev.addEventListener("click",()=>{

        current--;

        if(current<0){

            current=images.length-1;

        }

        showImage();

    });

});