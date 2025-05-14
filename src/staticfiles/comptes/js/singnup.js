const texts = ["S'enregistrer", "Créer un compte", "Rejoindre", "S'abonner", "Se joindre"]; // Liste des synonymes de "S'inscrire"
const speed = 150; // Vitesse d'écriture
const eraseSpeed = 100; // Vitesse d'effacement
const delay = 1500; // Pause avant effacement
const startEndColor = "#DB5E10"; // Couleur fixe pour début et fin
const colors = ["#F1A000", "#FF7F32", "#F3B03C", "#D4A400", "#FF6F20", "#C46E1F", "#DAB44D"]; // Couleurs qui vont bien avec #DB5E10

let textIndex = 0;
let index = 0;
let isDeleting = false;
let colorIndex = 0;
let currentColor = startEndColor;
const title = document.getElementById("animated-title");

function getNextColor() {
    return colors[colorIndex++ % colors.length]; // Prend une couleur unique par cycle
}

function getNextText() {
    return texts[textIndex++ % texts.length]; // Change le texte à chaque cycle
}

function typeEffect() {
    let currentText = texts[textIndex % texts.length];

    if (!isDeleting) {
        title.textContent = "🔑 " + currentText.substring(0, index++); // Ajouter l'emoji avant le texte
        if (index > currentText.length) {
            isDeleting = true;
            setTimeout(typeEffect, delay);
        } else {
            setTimeout(typeEffect, speed);
        }
    } else {
        title.textContent = "🔑 " + currentText.substring(0, index--); // Ajouter l'emoji avant le texte
        if (index < 0) {
            isDeleting = false;
            currentColor = getNextColor(); // Change la couleur après un cycle
            title.style.color = currentColor;
            textIndex++; // Passe au texte suivant
            setTimeout(typeEffect, speed);
        } else {
            setTimeout(typeEffect, eraseSpeed);
        }
    }
}

title.style.color = currentColor; // Appliquer la couleur initiale
typeEffect();