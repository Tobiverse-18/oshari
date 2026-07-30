const minus = document.querySelector(".minus");
const plus = document.querySelector(".plus");
const quantity = document.getElementById("quantity");

if(minus){

    minus.onclick = () =>{

        if(quantity.value > 1){

            quantity.value--;

        }

    }

}

if(plus){

    plus.onclick = () =>{

        quantity.value++;

    }

}