document.addEventListener("DOMContentLoaded", afficherPanier);

function afficherPanier() {
    let panier = JSON.parse(localStorage.getItem("panier")) || [];
    let listePanier = document.getElementById("liste_panier");
    let totalPrice = 0;
    listePanier.innerHTML = "";

    panier.forEach((produit, index) => {
        let prixProduit = parseFloat(produit.prix?.toString().replace(",", ".")) || 0;
        let quantite = produit.quantite || 1;
        let totalProduit = prixProduit * quantite;
        totalPrice += totalProduit;

        let li = document.createElement("li");
        li.classList.add("panier-item");
        li.dataset.index = index;
        li.innerHTML = `
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

function modifierQuantite(index, delta) {
    let panier = JSON.parse(localStorage.getItem("panier")) || [];

    if (panier[index]) {
        panier[index].quantite = (panier[index].quantite || 1) + delta;

        if (panier[index].quantite <= 0) {
            panier.splice(index, 1);
        }

        localStorage.setItem("panier", JSON.stringify(panier));
        afficherPanier();
    }
}

document.getElementById("validerCommande").addEventListener("click", function () {
    validerCommande();
});

function validerCommande() {
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
