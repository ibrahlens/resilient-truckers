console.log("JavaScript Loaded");

/* =====================================
   COUNTERS
===================================== */

const counters = document.querySelectorAll(".counter");

if (counters.length > 0) {

    const animateCounter = (counter) => {

        const target = parseInt(counter.dataset.target);

        if (isNaN(target)) return;

        let current = 0;
        const increment = Math.ceil(target / 120);

        function update() {

            current += increment;

            if (current < target) {

                counter.textContent = current.toLocaleString();
                requestAnimationFrame(update);

            } else {

                counter.textContent = target.toLocaleString() + "+";

            }

        }

        update();

    };

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                animateCounter(entry.target);
                observer.unobserve(entry.target);

            }

        });

    });

    counters.forEach(counter => observer.observe(counter));

}

/* =====================================
   SCROLL REVEAL
===================================== */

const reveals = document.querySelectorAll(".reveal");

function revealSections() {

    const windowHeight = window.innerHeight;

    reveals.forEach(section => {

        if (section.getBoundingClientRect().top < windowHeight - 100) {

            section.classList.add("active");

        }

    });

}

window.addEventListener("scroll", revealSections);

revealSections();

/* =====================================
   NAVBAR SCROLL
===================================== */

const navbar = document.querySelector(".navbar");

if (navbar) {

    window.addEventListener("scroll", () => {

        if (window.scrollY > 50) {

            navbar.classList.add("scrolled");

        } else {

            navbar.classList.remove("scrolled");

        }

    });

}

/* =====================================
   FLASH MESSAGES
===================================== */

setTimeout(() => {

    document.querySelectorAll(".flash-message").forEach(alert => {

        alert.style.transition = "all .5s";
        alert.style.opacity = "0";
        alert.style.transform = "translateX(100px)";

        setTimeout(() => {

            alert.remove();

        }, 500);

    });

}, 5000);

/* =====================================
   SETTINGS TABS
===================================== */

function openTab(tabId) {

    document.querySelectorAll(".settings-section").forEach(section => {

        section.classList.remove("active-tab");

    });

    document.querySelectorAll(".tab-btn").forEach(button => {

        button.classList.remove("active");

    });

    document.getElementById(tabId).classList.add("active-tab");

    event.currentTarget.classList.add("active");

}


document.addEventListener("DOMContentLoaded", function () {

    const flashMessages = document.querySelectorAll(".flash");

    flashMessages.forEach(function (message) {

        setTimeout(function () {

            message.style.opacity = "0";
            message.style.transform = "translateX(40px)";

            setTimeout(function () {
                message.remove();
            }, 400);

        }, 5000);

    });

});

document.addEventListener("DOMContentLoaded", function () {

    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");

    if (!menuToggle || !navLinks) {
        return;
    }

    menuToggle.addEventListener("click", function () {

        const isOpen = navLinks.classList.toggle("active");

        menuToggle.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );

        const icon = menuToggle.querySelector("i");

        if (icon) {
            icon.classList.toggle("fa-bars", !isOpen);
            icon.classList.toggle("fa-xmark", isOpen);
        }

    });

    /* Close menu after selecting a page */
    navLinks.querySelectorAll("a").forEach(function (link) {

        link.addEventListener("click", function () {

            navLinks.classList.remove("active");

            menuToggle.setAttribute(
                "aria-expanded",
                "false"
            );

            const icon = menuToggle.querySelector("i");

            if (icon) {
                icon.classList.remove("fa-xmark");
                icon.classList.add("fa-bars");
            }

        });

    });

});