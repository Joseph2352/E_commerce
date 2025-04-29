document.addEventListener("DOMContentLoaded", () => {
    afficherPanier();
    updatePanierCount();
});
function afficherPanier() {
    let panier = JSON.parse(localStorage.getItem("panier")) || [];
    let listePanier = document.getElementById("liste_panier");
    let listinfo = document.getElementById("listinfo");
    let totalPrice = 0;
    listePanier.innerHTML = "";
    listinfo.innerHTML = "";

    panier.forEach((produit, index) => {
        let prixProduit = parseFloat(produit.prix?.toString().replace(",", ".")) || 0;
        let quantite = produit.quantite || 1;
        let totalProduit = prixProduit * quantite;
        totalPrice += totalProduit;

        let li = document.createElement("li");
        li.classList.add("panier-item");
        li.dataset.index = index;
        li.innerHTML = `
            <input type="checkbox" class="checkbox-produit" data-index="${index}" checked />
            <img src="${produit.image}" alt="${produit.nom}" class="produit-image">
            <span class="produit-details">
                <strong>${produit.nom || "Produit inconnu"}</strong> - 
                <span class="produit-prix">${prixProduit.toFixed(2)}</span> €  
            </span>
            <div class="quantite-controls">
                <button class="btn-moins" onclick="modifierQuantite(${index}, -1)">-</button>
                <span class="quantite">${quantite}</span>
                <button class="btn-plus" onclick="modifierQuantite(${index}, 1)">+</button>
            </div>
        `;

        listePanier.appendChild(li);
    });

    document.getElementById("total_price").innerText = totalPrice.toFixed(2);
}

document.getElementById("validerCommande").addEventListener("click", function () {
    let panier = JSON.parse(localStorage.getItem("panier")) || [];
    let produitsSelectionnes = [];

    // On récupère tous les checkboxes cochés
    document.querySelectorAll(".checkbox-produit:checked").forEach(checkbox => {
        let index = checkbox.dataset.index;
        if (panier[index]) {
            produitsSelectionnes.push(panier[index]);
        }
    });

    console.log("Produits sélectionnés pour la commande:", produitsSelectionnes);

    if (produitsSelectionnes.length === 0) {
        alert("Veuillez sélectionner au moins un produit pour continuer.");
        return;
    }

    // 🔥 Sauvegarder les produits sélectionnés
    localStorage.setItem("produits_a_commander", JSON.stringify(produitsSelectionnes));

    console.log(CHECKOUT_URL);
    // 🔥 Rediriger vers la page de commande
    window.location.href = CHECKOUT_URL;
});


function updatePanierCount() {
    let panier = JSON.parse(localStorage.getItem("panier")) || [];
    let compteur = document.querySelectorAll(".compteur_panier");
    if (compteur.length > 0) {
        compteur.forEach(element => {
            element.innerText = panier.length > 0 ? panier.length : "0";
        });
    }
}

function modifierQuantite(index, delta) {
    let panier = JSON.parse(localStorage.getItem("panier")) || [];

    if (panier[index]) {
        panier[index].quantite = (panier[index].quantite || 1) + delta;

        if (panier[index].quantite <= 0) {
            panier.splice(index, 1);
        }

        localStorage.setItem("panier", JSON.stringify(panier));
        afficherPanier();
        updatePanierCount();   
    }
}




function chargerPanierDepuisServeur() {
    fetch(GET_PANIER_URL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie('csrftoken')  // Ajouter CSRF token ici pour plus de sécurité
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Erreur lors de la récupération du panier.");
    })
    .then(data => {
        if (data.panier && data.panier.length > 0) {
            console.log("Panier récupéré depuis le serveur:", data.panier);
            localStorage.setItem("panier", JSON.stringify(data.panier));
            afficherPanier();
            updatePanierCount();
        }
    })
    .catch(error => {
        console.error("Erreur:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    if (isUserLoggedIn()) {
        chargerPanierDepuisServeur(); // 🔥 Récupérer depuis la base de données
    } else {
        afficherPanier(); // Si pas connecté, afficher ce qu'il y a en localStorage
    }
    updatePanierCount();
});


/*
document.getElementById("validerCommande").addEventListener("click", function () {
    validerCommande();
});

    let panier = JSON.parse(localStorage.getItem("panier")) || [];
    if (panier.length === 0) {
        alert("Votre panier est vide !");
        return;
    }

    fetch("/produit/confirm-order/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ cart: panier })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            localStorage.removeItem("panier");
            if (data.payment_url) {
                window.location.href = data.payment_url;  // ✅ Redirection vers Paycard
            } else {
                alert("Erreur: URL de paiement invalide !");
            }
        } else {
            alert("Erreur lors de la commande !");
        }
    })
    .catch(error => console.error("Erreur :", error));
}

function getCSRFToken() {
    let tokenElement = document.querySelector('[name=csrf-token]');
    return tokenElement ? tokenElement.getAttribute('content') : "";
}
*/
