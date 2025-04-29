document.addEventListener("DOMContentLoaded", function () {
    // Vérifie si "panier" existe dans le localStorage et est un tableau valide
    let panier = JSON.parse(localStorage.getItem("panier"));
    if (!Array.isArray(panier)) {
        panier = [];  // Si ce n'est pas un tableau, initialise-le comme un tableau vide
    }

    function updatePanierCount() {
        let compteur = document.querySelectorAll(".compteur_panier");
        if (compteur.length > 0) {
            compteur.forEach(element => {
                element.innerText = panier.length > 0 ? panier.length : "0"; // Affiche un nombre ou rien si 0
            });
        }
    }

    function ajouterAuPanier(id, nom, prix, image) {
        let produit = { id, nom, prix, image };
        const message = document.querySelector(".verifie_produit_exist");
        const message_confirm = document.querySelector('.ajout_succes')
        let existe = panier.find(item => item.id === id);
        if (!existe) {
            panier.push(produit);
            localStorage.setItem("panier", JSON.stringify(panier));
            updatePanierCount();
            message_confirm.style.display = "flex";
            message_confirm.style.opacity = "0";

            setTimeout(() => {
                message_confirm.style.transition = "opacity 0.5s";
                message_confirm.style.opacity = "1";

                // Après 1 seconde (1000ms), faire disparaître
                setTimeout(() => {
                    message_confirm.style.opacity = "0";
                    
                    // Une fois l'animation terminée (0.5s), cacher le display
                    setTimeout(() => {
                        message_confirm.style.display = "none";
                    }, 500);
                }, 1000);

            }, 10);

        } else {
            message.style.display = "flex";
            message.style.opacity = "0";
            setTimeout(() => {
                message.style.transition = "opacity 0.5s";
                message.style.opacity = "1";
            }, 10); // Petit délai pour permettre l'affichage initial
            
        }
    }

    // Attacher l'événement de clic à toutes les divs avec la classe "ajouter-panier"
    document.querySelectorAll(".ajouter-panier").forEach(div => {
        div.addEventListener("click", function () {
            let id = this.dataset.id;
            let nom = this.dataset.nom;
            let prix = this.dataset.prix;
            let image = this.dataset.image;
            ajouterAuPanier(id, nom, prix, image);
        });
    });

    updatePanierCount(); // Met à jour le compteur dès le début
});

let panier = JSON.parse(localStorage.getItem("panier")) || [];
console.log('Contenu du panier avant envoi:', panier); 

document.addEventListener("DOMContentLoaded", function () {
    const panierIcone = document.querySelector(".iconcon.icon");

    if (panierIcone) {
        panierIcone.addEventListener("click", function (e) {
            e.preventDefault(); // On bloque la redirection immédiate

            let panier = JSON.parse(localStorage.getItem("panier")) || [];

            panier = panier.map(item => ({
                id: item.id,
                nom: item.nom,
                prix: parseFloat(item.prix.replace(',', '.')), // Corrige prix
                quantite: item.quantite ? item.quantite : 1,    // Ajoute quantite si absente
                image: item.image
            }));
            
            fetch(SYNC_PANIER_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie('csrftoken')
                },
                body: JSON.stringify({ cart: panier })
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Erreur lors de la synchronisation du panier.');
            })
            .then(data => {
                console.log(data.message);
                window.location.href = PANIER_URL;
            })
            .catch(error => {
                console.error(error);
                window.location.href = PANIER_URL;
            });
            
        });
    }

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
});

document.addEventListener("DOMContentLoaded", function () {
    // Vérifier si l'utilisateur est connecté (par exemple via un cookie ou un élément de session)
    if (isUserLoggedIn()) {
        let panier = JSON.parse(localStorage.getItem("panier")) || [];
        
        // Si le panier n'est pas vide, on le synchronise avec le serveur
        if (panier.length > 0) {
            syncPanierAvecServeur(panier);
        }
    }
});

function isUserLoggedIn() {
    // Vérifie si l'utilisateur est connecté (par exemple, un cookie ou une variable de session)
    // Adapte ceci selon la façon dont ton backend gère la session
    return document.body.classList.contains("user-logged-in"); // Exemple avec une classe dans le body
}


function syncPanierAvecServeur() {
    let panier = JSON.parse(localStorage.getItem("panier")) || [];

    console.log("Contenu du panier avant envoi:", panier);

    fetch(SYNC_PANIER_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({ cart: panier })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Erreur lors de la synchronisation du panier.');
    })
    .then(data => {
        console.log(data.message);
        window.location.href = PANIER_URL;
    })
    .catch(error => {
        console.error(error);
        window.location.href = PANIER_URL;
    });
}

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


