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