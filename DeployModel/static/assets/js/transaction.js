const links = document.getElementById("links");
const dropdownnav = document.getElementById("dropdownnav");
const hamburger = document.getElementById("hamburger");
const line_separator = document.getElementById("line-separator");

if (screen.width >= 550) {
    hamburger.style.display = "none";
}
// if (screen.width <= 550) {
//     line_separator.style.width = "60vw";
//     line_separator.style.height = "0.5px";
//     line_separator.style.top = "50%";
//     line_separator.style.transform = "translate(-50%, -50%)";
// }
window.addEventListener("resize", () => {
    if (screen.width < 550) {
        hamburger.style.display = "flex";
        // line_separator.style.width = "60vw";
        // line_separator.style.height = "0.5px";
        // line_separator.style.top = "50%";
        // line_separator.style.transform = "translate(-50%, -50%)";
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