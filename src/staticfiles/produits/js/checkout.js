document.addEventListener("DOMContentLoaded", function () {
    const produits = JSON.parse(localStorage.getItem("produits_a_commander")) || [];
    const listeCommande = document.getElementById("liste_commande");
    const listInfo = document.getElementById("listinfo");
    let prixTotal = 0;

    listeCommande.innerHTML = "";

    produits.forEach((produit, index) => {
        const prixProduit = parseFloat((produit.prix || "0").toString().replace(",", ".")) || 0;
        const quantite = produit.quantite || 1;
        const totalProduit = prixProduit * quantite;
        prixTotal += totalProduit;

        // Ajout dans l'affichage de la liste
        const li = document.createElement("li");
        li.classList.add("commande-item");
        li.innerHTML = `
            <img src="${produit.image || '#'}" alt="${produit.nom || 'Produit inconnu'}" class="commande-image">
            <div class="box">
                <div class="commande-details">
                    <h4>${produit.nom || "Produit inconnu"}</h4>
                    <p>Prix: ${prixProduit.toFixed(2)} $US</p>
                    <p>Quantité: <span class="quantite">${quantite}</span></p>
                    <p>Total: ${totalProduit.toFixed(2)} $US</p>
                </div>
                <div class="quantite-controls">
                    <button class="btn-moins" data-index="${index}" data-action="-1">-</button>
                    <button class="btn-plus" data-index="${index}" data-action="1">+</button>
                </div>
            </div>
        `;
        listeCommande.appendChild(li);

        // Ajout dans les inputs cachés du formulaire
        listInfo.innerHTML += `
            <input type="hidden" name="produits[${index}][nom]" value="${produit.nom}">
            <input type="hidden" name="produits[${index}][prix]" value="${produit.prix}">
            <input type="hidden" name="produits[${index}][quantite]" value="${produit.quantite}">
        `;
    });

    document.getElementById("prix_total_commande").innerText = prixTotal.toFixed(2);
    document.getElementById("sous_total_commande").innerText = prixTotal.toFixed(2);

    listeCommande.addEventListener("click", function (e) {
        if (e.target.matches(".btn-moins, .btn-plus")) {
            const index = parseInt(e.target.getAttribute("data-index"));
            const delta = parseInt(e.target.getAttribute("data-action"));
            modifierQuantite(index, delta);
        }
    });

    document.getElementById("confirmerCommande").addEventListener("click", function () {
        // Cache le bouton
        this.style.display = "none";
    
        // Affiche le spinner
        document.getElementById("loadingSpinner").style.display = "block";
    
        // Vide le panier dans le localStorage (important)
        localStorage.removeItem("produits_a_commander");
    });
});

function modifierQuantite(index, delta) {
    const produits = JSON.parse(localStorage.getItem("produits_a_commander")) || [];

    if (produits[index]) {
        produits[index].quantite = (produits[index].quantite || 1) + delta;

        if (produits[index].quantite <= 0) {
            produits.splice(index, 1);
        }

        localStorage.setItem("produits_a_commander", JSON.stringify(produits));
        window.location.reload();
    }
}
