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

function updatePanierCount() {
    let panier = JSON.parse(localStorage.getItem("panier")) || [];
    let compteur = document.querySelectorAll(".compteur_panier");
    if (compteur.length > 0) {

        compteur.forEach(element => {
            element.innerText = panier.length > 0 ? panier.length : "0"; // Affiche un nombre ou rien si 0
            console.log(panier.length)
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

    afficherPanier();