document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menubtn");
    const menuBox = document.querySelector(".menbox");
    const menuCloseBtn = document.querySelector("#menubtn2 button");

    function openMenu() {
        menuBox.classList.add("open");
        menuBtn.classList.add("active");
        document.body.classList.add("scroll"); // Désactive le défilement
    }

    function closeMenu() {
        menuBox.classList.remove("open");
        menuBtn.classList.remove("active");
        document.body.classList.remove("no-scroll"); // Réactive le défilement
    }

    menuBtn.addEventListener("click", function () {
        if (menuBox.classList.contains("open")) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    menuCloseBtn.addEventListener("click", closeMenu);

    document.addEventListener("click", function (event) {
        if (!menuBox.contains(event.target) && !menuBtn.contains(event.target)) {
            closeMenu();
        }
    });

    menuBox.addEventListener("click", function (event) {
        event.stopPropagation();
    });
});


// Vérifie si la taille de l'écran est supérieure à 1200px
if (window.innerWidth > 1200) {
    let hoverElements = document.querySelectorAll('.hover-container');

    // Boucle sur chaque élément pour ajouter des événements de survol
    hoverElements.forEach((hoverElement, index) => {
        let hiddenPage = document.getElementById('hiddenPage' + (index + 1)); 
        
        hoverElement.addEventListener("mouseover", function() {
            hiddenPage.style.visibility = "visible"; 
            hiddenPage.style.opacity = "1";
            hiddenPage.style.height = "auto";
        });
        hiddenPage.addEventListener("mouseover", function() {
            hiddenPage.style.visibility = "visible";
            hiddenPage.style.opacity = "1"; 
            hiddenPage.style.height = "auto";
        });

        hoverElement.addEventListener("mouseout", function() {
            hiddenPage.style.visibility = "hidden"; 
            hiddenPage.style.opacity = "0"; 
            hiddenPage.style.height = "0";
        });
        hiddenPage.addEventListener("mouseout", function() {
            hiddenPage.style.visibility = "hidden"; 
            hiddenPage.style.opacity = "0"; 
            hiddenPage.style.height = "0";
        });
    });
}

function toggleDropdown() {
    var dropdown = document.getElementById("profileDropdown");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

// Fermer le menu si on clique ailleurs
document.addEventListener("click", function(event) {
    var dropdown = document.getElementById("profileDropdown");
    var profile = document.querySelector(".profile-container");
    if (!profile.contains(event.target)) {
        dropdown.style.display = "none";
    }
});