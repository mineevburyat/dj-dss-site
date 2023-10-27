const burger = document.querySelector(".burger");
const close = document.querySelector(".close-btn");
const menu = document.querySelector(".menu-none");

burger.addEventListener('click', () => {
    menu.classList.add("menu--active");
})
close.addEventListener('click', () => {
    menu.classList.remove("menu--active");
})