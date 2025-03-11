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

document.querySelector('.box_recher').addEventListener('click', function (event) {
    // Éviter que le clic sur .box_recher déclenche la fermeture
    event.stopPropagation();
    this.classList.toggle('expanded');
  });
  
  // Écouter les clics sur le document pour fermer .box_recher si on clique en dehors
  document.addEventListener('click', function (event) {
    var boxRecher = document.querySelector('.box_recher');
    
    // Vérifie si le clic est à l'extérieur de .box_recher
    if (!boxRecher.contains(event.target)) {
      boxRecher.classList.remove('expanded');
    }
  });


document.addEventListener("DOMContentLoaded", function () {
    if (window.innerWidth > 1200) { 
        let hoverElements = document.querySelectorAll('.hover-container');

        hoverElements.forEach((hoverElement, index) => {
            let hiddenPage = document.getElementById('hiddenPage' + (index + 1));

            hoverElement.addEventListener("mouseover", function() {
                showHiddenPage(hiddenPage);
            });

            hoverElement.addEventListener("mouseout", function() {
                hideHiddenPage(hiddenPage);
            });

            hiddenPage.addEventListener("mouseover", function() {
                showHiddenPage(hiddenPage);
            });

            hiddenPage.addEventListener("mouseout", function() {
                hideHiddenPage(hiddenPage);
            });
        });

        function showHiddenPage(hiddenPage) {
            hiddenPage.style.visibility = "visible";
            hiddenPage.style.opacity = "1";
            hiddenPage.style.height = "auto";
        }

        function hideHiddenPage(hiddenPage) {
            hiddenPage.style.visibility = "hidden";
            hiddenPage.style.opacity = "0";
            hiddenPage.style.height = "0";
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("profileDropdown");
    const profile = document.querySelector(".profile-container");

    // Fermer le menu si on clique ailleurs
    document.addEventListener("click", function(event) {
        if (!profile.contains(event.target)) {
            dropdown.style.display = "none";
        }
    });

    // Ouvrir le menu lorsque l'on clique sur le profil
    profile.addEventListener("click", function(event) {
        event.stopPropagation(); // Empêche la propagation de l'événement de clic
        dropdown.style.display = dropdown.style.display === "flex" ? "none" : "flex";
    });
});