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
        let existe = panier.find(item => item.id === id);
        if (!existe) {
            panier.push(produit);
            localStorage.setItem("panier", JSON.stringify(panier));
            updatePanierCount();
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
