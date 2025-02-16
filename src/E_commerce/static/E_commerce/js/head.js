document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menubtn");
    const menuBox = document.querySelector(".menbox");
    const menuCloseBtn = document.querySelector("#menubtn2 button");

    function openMenu() {
        menuBox.classList.add("open");
        menuBtn.classList.add("active");
        document.body.classList.add("no-scroll"); // Désactive le défilement
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

// Acategorie hover
let hoverElements = document.querySelectorAll('.hover-container');
      
    // Boucle sur chaque élément pour ajouter des événements de survol
    hoverElements.forEach((hoverElement, index) => {
        let hiddenPage = document.getElementById('hiddenPage' + (index + 1)); // Associer la page cachée à l'élément correspondant
        
        hoverElement.addEventListener("mouseover", function() {
            hiddenPage.style.height = "400px"; // Ajuste selon la taille de l'iframe
        });
        hiddenPage.addEventListener("mouseover", function() {
            hiddenPage.style.height = "400px"; // Ajuste selon la taille de l'iframe
        });

        hoverElement.addEventListener("mouseout", function() {
            hiddenPage.style.height = "0";
        });
        hiddenPage.addEventListener("mouseout", function() {
            hiddenPage.style.height = "0";
        });
    });