from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.timezone import now


# Vue de connexion
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil après connexion
        else:
            # Si l'utilisateur n'est pas trouvé
            return render(request, 'comptes/login.html', {'error': 'Identifiants invalides'})

    return render(request, 'comptes/login.html',{'static_version':now().timestamp()})


# Vue d'inscription
def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not first_name:  # Vérifie si fullname est vide
            error = "Le champ Prenom complet est obligatoire."
        if not last_name:  # Vérifie si fullname est vide
            error = "Le champ Nom complet est obligatoire."
        # Vérifier si les mots de passe correspondent
        if password1 != password2:
            return render(request, 'comptes/singup.html', {'error': 'Les mots de passe ne correspondent pas'})

        # Vérifier si l'utilisateur existe déjà
        User = get_user_model()  # Récupère le modèle utilisateur personnalisé
        if User.objects.filter(username=username).exists():
            return render(request, 'comptes/singup.html', {'error': 'Ce nom d\'utilisateur est déjà pris'})

        # Créer un nouvel utilisateur
        user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
                )
        user.save()
        login(request, user)  # Connexion automatique après inscription
        return redirect('login')  # Redirige vers la page d'accueil après inscription

    return render(request, 'comptes/singup.html',{'static_version':now().timestamp()}) 

@login_required
def profil_view(request):
    return render(request, 'profil.html')