const ta = document.getElementById("ta");
const ma = document.getElementById("ma");
const it = document.getElementById("it");

// ta.addEventListener("click", () => {
//     transaction();
// })
// ma.addEventListener("click", () => {
//     mixer();
// })
// it.addEventListener("click", () => {
//     illicit();
// })

// const transaction = () => {
//     window.location.replace("./templates/transaction.html");
// }
// const mixer = () => {
//     window.location.replace("./templates/mixer.html");
// }
// const illicit = () => {
//     window.location.replace("./templates/illicit.html");
// }



const links = document.getElementById("links");
const dropdownnav = document.getElementById("dropdownnav");
const hamburger = document.getElementById("hamburger");

if (screen.width >= 550) {
    hamburger.style.display = "none";
}
window.addEventListener("resize", () => {
    if (screen.width < 550) {
        hamburger.style.display = "flex";
    }
    if (screen.width >= 550) {
        hamburger.style.display = "none";
    }
})

hamburger.addEventListener("click", () => {
    if (dropdownnav.style.display != "flex" && screen.width <= 550) {
        dropdownnav.style.display = "flex";
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
})
