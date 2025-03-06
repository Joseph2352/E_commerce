<<<<<<< HEAD
<<<<<<< HEAD
# E-Commerce
=======
>>>>>>> 275053d (Troisieme commit: gestion du panier)
E_commerce

Description

E_commerce est une application web développée avec Django permettant aux utilisateurs d'acheter des produits en ligne. Elle comprend la gestion des utilisateurs, des produits, des commandes et un panier interactif grâce à JavaScript.

Installation

Prérequis

Python 3.x

pip

Étapes d'installation

Cloner le dépôt

<<<<<<< HEAD
git clone <URL_DU_REPO>
cd E_commerce

Créer et activer un environnement virtuel 

python3 -m venv .env
source .env/bin/activate  # Sous Windows : venv\Scripts\activate
=======
git clone <URL_DU_REPO> cd E_commerce

Créer et activer un environnement virtuel

python3 -m venv .env source .env/bin/activate # Sous Windows : venv\Scripts\activate
>>>>>>> 275053d (Troisieme commit: gestion du panier)

Installer les dépendances

deplacé vous dans le repertoir src

pip install -r requirements.txt

Appliquer les migrations de la base de données

python manage.py migrate

Lancer le serveur

python manage.py runserver

<<<<<<< HEAD
Accéder à l'application
Ouvrir un navigateur et aller sur http://127.0.0.1:8000/
=======
Accéder à l'application Ouvrir un navigateur et aller sur http://127.0.0.1:8000/
>>>>>>> 275053d (Troisieme commit: gestion du panier)

Fonctionnalités

Gestion des utilisateurs (inscription, connexion, déconnexion)

Affichage des produits

Ajout de produits au panier

Passage de commandes

Interface d'administration Django pour gérer les produits et commandes

Technologies utilisées

Django (Backend)

JavaScript (pour le panier interactif)

SQLite (par défaut, mais peut être remplacé par PostgreSQL ou MySQL)

HTML/CSS pour le frontend

Contribution

Fork du projet

Création d'une branche : git checkout -b feature-nouvelle-fonctionnalité

Ajout et commit des modifications : git commit -m "Ajout d'une nouvelle fonctionnalité"

Push vers le dépôt distant : git push origin feature-nouvelle-fonctionnalité

Création d'une pull request

Auteur

Mamy Joseph
<<<<<<< HEAD


=======
 E-Commerce
>>>>>>> d9e6bf6 (Troisieme commit: gestion du panier)
=======
>>>>>>> 275053d (Troisieme commit: gestion du panier)
