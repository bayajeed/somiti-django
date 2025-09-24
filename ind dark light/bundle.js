document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  // ======= Sticky Menu Logic =======
  const header = document.querySelector(".header");
  if (header) {
    const sticky = header.offsetTop;
    window.onscroll = function () {
      if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
      } else {
        header.classList.remove("sticky");
      }
    };
  }

  // ======= Dark & Light Mode Toggler =======
  const darkTogglerCheckbox = document.querySelector("#darkToggler");
  const html = document.querySelector("html");

  if (darkTogglerCheckbox && html) {
    const darkModeToggler = () => {
      if (darkTogglerCheckbox.checked) {
        html.setAttribute("data-bs-theme", "dark");
      } else {
        html.setAttribute("data-bs-theme", "light");
      }
    };
    darkModeToggler(); // Initialize based on checkbox state
    darkTogglerCheckbox.addEventListener("change", darkModeToggler);
  }

  // ======= Mobile Menu Logic =======
  const menuToggler = document.querySelector(".menu-toggler");
  const menuWrapper = document.querySelector(".menu-wrapper");

  if (menuToggler && menuWrapper) {
    const toggleMenu = () => {
      menuWrapper.classList.toggle("show");
      document.body.classList.toggle("overflow-hidden");
      menuToggler.querySelector(".cross").classList.toggle("d-none");
      menuToggler.querySelector(".menu").classList.toggle("d-none");
    };

    menuToggler.addEventListener("click", toggleMenu);

    document.querySelectorAll(".navbar-nav .nav-item:not(.dropdown) a").forEach(link => {
      link.addEventListener("click", () => {
        if (menuWrapper.classList.contains("show")) {
          toggleMenu();
        }
      });
    });
  }
});