if (navigator.userAgent.includes("Windows")) {
    document.body.style.zoom = "85%";
} else {
    document.body.style.zoom = "100%"; // Remet à la normale sur Kali
}

// Version robuste de ajout_favori.js
async function toggleFavori(produitId) {
    const isAuthenticated = document.body.getAttribute('data-is-authenticated') === 'true';
    
    if (isAuthenticated) {
        try {
            const csrfToken = getCookie('csrftoken');
            if (!csrfToken) {
                throw new Error('CSRF token manquant');
            }

            const response = await fetch(`${TOGGLE_FAVORI_URL}${produitId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Erreur serveur');
            }

            const data = await response.json();
            return data.liked;
            
        } catch (error) {
            console.error('Erreur:', error);
            alert(error.message);
            return false;
        }
    }  else {
        return new Promise((resolve) => {
            try {
                let favoris = JSON.parse(localStorage.getItem('favoris') || '[]');
                const index = favoris.findIndex(p => p.id === produitId);
                
                if (index === -1) {
                    favoris.push({
                        id: produitId,
                    });
                } else {
                    favoris.splice(index, 1);
                }
                
                localStorage.setItem('favoris', JSON.stringify(favoris));
                resolve(index === -1);
            } catch (error) {
                console.error('Error with localStorage:', error);
                resolve(false);
            }
        });
    }
}

async function syncFavoris() {
    const favoris = JSON.parse(localStorage.getItem('favoris')) || [];
    
    if (favoris.length === 0) return;
    
    try {
        const response = await fetch(SYNC_FAVORIS_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ favoris })
        });
        
        if (response.ok) {
            localStorage.removeItem('favoris');
            console.log('Favoris synchronisés avec succès');
        } else {
            console.error('Échec de la synchronisation:', response.status);
        }
    } catch (error) {
        console.error('Error syncing favorites:', error);
    }
}
// Mise à jour de l'icône cœur
function updateHeartIcon(button, isFavori) {
    const outline = button.querySelector('.heart-outline');
    const filled = button.querySelector('.heart-filled');
    
    if (isFavori) {
        outline.style.display = 'none';
        filled.style.display = 'inline';
    } else {
        outline.style.display = 'inline';
        filled.style.display = 'none';
    }
}

// Fonction pour récupérer le cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialisation des boutons favoris
function initFavorisButtons() {
    const buttons = document.querySelectorAll('.favoriplus.ajouter-favori');
    if (buttons.length === 0) {
        console.warn('Aucun bouton favori trouvé');
        return;
    }

    buttons.forEach(button => {
        const produitId = button.dataset.id;
        const liElement = button.closest('li');
        
        if (!liElement) {
            console.warn('Élément li parent non trouvé pour le bouton favori');
            return;
        }
        
        const isAuthenticated = document.body.getAttribute('data-is-authenticated') === 'true';
        let isFavori = false;
        
        // Vérification initiale plus robuste
        if (isAuthenticated) {
            // Pour les utilisateurs connectés, on utilise directement l'attribut data-is-favori
            // qui devrait être défini par le template Django
            const favoriState = liElement.getAttribute('data-is-favori');
            if (favoriState !== null) {
                isFavori = favoriState === 'true';
            } else {
                console.warn('Attribut data-is-favori manquant pour le produit', produitId);
                // Fallback: vérification visuelle des icônes
                const filled = button.querySelector('.heart-filled').style.display !== 'none';
                isFavori = filled;
            }
        } else {
            // Pour les utilisateurs non connectés, on utilise le localStorage
            try {
                const favoris = JSON.parse(localStorage.getItem('favoris')) || [];
                isFavori = favoris.some(p => p.id.toString() === produitId.toString());
                // On synchronise l'attribut data avec le localStorage
                liElement.setAttribute('data-is-favori', isFavori.toString());
            } catch (error) {
                console.error('Erreur lecture localStorage:', error);
            }
        }
        
        // Mise à jour initiale de l'icône
        updateHeartIcon(button, isFavori);
        
        // Gestion du clic
        button.addEventListener('click', async function(event) {
            event.stopPropagation();
            event.preventDefault();
            
            const wasAdded = await toggleFavori(
                produitId,
                button.dataset.nom,
                button.dataset.prix,
                button.dataset.image,
                button.dataset.detail
            );
            
            // Mise à jour de l'interface
            updateHeartIcon(button, wasAdded);
            liElement.setAttribute('data-is-favori', wasAdded.toString());
            
            // Pour le débogage
            console.log(`Produit ${produitId} - Favori: ${wasAdded}`, {
                auth: isAuthenticated,
                storedState: liElement.getAttribute('data-is-favori')
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Initialisation des favoris...');
    console.log('TOGGLE_FAVORI_URL:', TOGGLE_FAVORI_URL);
    console.log('SYNC_FAVORIS_URL:', SYNC_FAVORIS_URL);
    
    const isAuthenticated = document.body.hasAttribute('data-is-authenticated') && 
                          document.body.getAttribute('data-is-authenticated') === 'true';
    
    if (isAuthenticated && localStorage.getItem('favoris')) {
        console.log('Synchronisation des favoris locaux...');
        syncFavoris();
    }
    
    initFavorisButtons();
});

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
    // Fermer le menu si on clique en dehors du menu et du bouton
    document.addEventListener("click", function (event) {
        if (!menuBox.contains(event.target) && !menuBtn.contains(event.target)) {
            closeMenu();
        }
    });

    // Empêche la propagation du clic à l'intérieur du menu
    menuBox.addEventListener("click", function (event) {
        event.stopPropagation();
    });
});

document.addEventListener("DOMContentLoaded", function () {
    let menuBtnSupers = document.querySelectorAll(".menubtn_super_categorie");
   
    menuBtnSupers.forEach((menuBtnSuper, index) => {
        let menuBoxSuper = document.getElementById('menbox_super_categorie' + (index + 1 ));
        const menuCloseBtnSuper = menuBoxSuper.querySelector("button");

        function openMenuSuper() {
            menuBoxSuper.classList.add("open");
            menuBtnSuper.classList.add("active");
            document.body.classList.add("no-scroll");
        }
        function closeMenuSuper() {
            menuBoxSuper.classList.remove("open");
            menuBtnSuper.classList.remove("active");
            document.body.classList.remove("no-scroll");
        }
        menuBtnSuper.addEventListener("click", function () {
            if (menuBoxSuper.classList.contains("open")) {
                closeMenuSuper();
            } else {
                openMenuSuper();
            }
        });
    
        menuCloseBtnSuper.addEventListener("click", closeMenuSuper);
        
        document.addEventListener("click", function (event) {
            if (!menuBoxSuper.contains(event.target) && !menuBtnSuper.contains(event.target)) {
                closeMenuSuper();
            }
        });

        menuBoxSuper.addEventListener("click", function (event) {
            event.stopPropagation();
        });
    });
});



document.querySelector('.box_recher').addEventListener('click', function (event) {
    // Éviter que le clic sur .box_recher déclenche la fermeture
    const annonce = document.querySelector('.annonce');
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


