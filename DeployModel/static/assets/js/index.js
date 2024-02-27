const ta = document.getElementById("ta");
const ma = document.getElementById("ma");
const it = document.getElementById("it");

<<<<<<< HEAD
ta.addEventListener("click", () => {
    transaction();
})
ma.addEventListener("click", () => {
    mixer();
})
it.addEventListener("click", () => {
    illicit();
})

const transaction = () => {
    window.location.replace("./templates/transaction.html");
}
const mixer = () => {
    window.location.replace("./templates/mixer.html");
}
const illicit = () => {
    window.location.replace("./templates/illicit.html");
=======
// ta.addEventListener("click", () => {
//     wip();
// })
ma.addEventListener("click", () => {
    wip();
})
it.addEventListener("click", () => {
    wip();
})

const wip = () => {
    window.location.replace("./notfound.html");
>>>>>>> d24460293c9dc51eb405d0ea47162381a6b36a9d
}



const links = document.getElementById("links");
const dropdownnav = document.getElementById("dropdownnav");
const hamburger = document.getElementById("hamburger");

if (screen.width >= 550) {
    hamburger.style.display = "none";
}
window.addEventListener("resize", () => {
    if (screen.width < 550) {
<<<<<<< HEAD
        hamburger.style.display = "flex";
=======
        hamburger.style.display = "block";
>>>>>>> d24460293c9dc51eb405d0ea47162381a6b36a9d
    }
    if (screen.width >= 550) {
        hamburger.style.display = "none";
    }
})

hamburger.addEventListener("click", () => {
<<<<<<< HEAD
    if (dropdownnav.style.display != "flex" && screen.width <= 550) {
        dropdownnav.style.display = "flex";
=======
    if (dropdownnav.style.display != "block" && screen.width <= 550) {
        dropdownnav.style.display = "block";
>>>>>>> d24460293c9dc51eb405d0ea47162381a6b36a9d
    } else {
        dropdownnav.style.display = "none";
    }

})




const getstarted1 = document.getElementById("getstarted1");
const getstarted2 = document.getElementById("getstarted2");
const getstarted3 = document.getElementById("getstarted3");

getstarted1.addEventListener("click", () => {
    window.location = "#content";
})
getstarted2.addEventListener("click", () => {
    window.location = "#content";
})
getstarted3.addEventListener("click", () => {
    window.location = "#content";
<<<<<<< HEAD
})
=======
})
>>>>>>> d24460293c9dc51eb405d0ea47162381a6b36a9d
