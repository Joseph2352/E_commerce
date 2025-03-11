from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.contrib.auth import update_session_auth_hash
import re
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

#-----------------------------------Vue  de connexion---------------------------------------------#
def log_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'comptes/login.html', {'error': 'Identifiants ou mot de passe incorrects'})

    return render(request, 'comptes/login.html', {'static_version': now().timestamp()})

#-----------------------------------Vue  d'inscription---------------------------------------------#
def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not first_name:
            error = "le champ nom est obligatoire."
            return render(request, 'comptes/singnup.html', {'first_name_error': error})
        if not last_name:
            error = "le champ prenom complet est obligatoire."
            return render(request, 'comptes/singnup.html', {'last_name_error': error})
        if password1 != password2:
            return render(request, 'comptes/singnup.html', {'error': 'les mots de passe ne correspondent pas.'})
        if not password1 or not password2:
            error = "le champ mot de passe est obligatoire."
            return render(request, 'comptes/singnup.html', {'error': error})
        else:
            # Password validation
            if len(password1) < 8:
                return render(request, 'comptes/singnup.html', {'error': 'Le mot de passe doit contenir au moins 8 caractères'})
            if not re.search(r'[A-Z]', password1):
                return render(request, 'comptes/singnup.html', {'error': 'Le mot de passe doit contenir au moins une lettre majuscule'})
            if not re.search(r'[a-z]', password1):
                return render(request, 'comptes/singnup.html', {'error': 'Le mot de passe doit contenir au moins une lettre minuscule'})
            if not re.search(r'[0-9]', password1):
                return render(request, 'comptes/singnup.html', {'error': 'Le mot de passe doit contenir au moins un chiffre'})
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
                return render(request, 'comptes/singnup.html', {'error': 'Le mot de passe doit contenir au moins un caractère spécial'})

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            return render(request, 'comptes/singnup.html', {'error': 'Cet email est déjà utilisé'})

        user = User.objects.create_user(
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        login(request, user)
        return redirect('confirmation_creat_compte')

    return render(request, 'comptes/singnup.html', {'static_version': now().timestamp()})

#-----------------------------------Vue de profil---------------------------------------------#
@login_required
def profil_view(request):
    return render(request, 'profil.html') 

#-----------------------------------------changement de mot de passe---------------------------------------------#
@login_required
def changePassword(request):
    if request.method == "POST":
        old_pwd = request.POST.get('ancien')
        new_pwd1 = request.POST.get('new1')
        new_pwd2 = request.POST.get('new2')
        
        if not old_pwd or not new_pwd1 or not new_pwd2:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'comptes/changePassword.html')
        
        if new_pwd1 != new_pwd2:
            nouveau = "Les nouveaux mots de passe ne correspondent pas."
            return render(request, 'comptes/changePassword.html', {'nouveau': nouveau})
        
        if not request.user.check_password(old_pwd):
            ancien = "L'ancien mot de passe est incorrect."
            return render(request, 'comptes/changePassword.html', {'ancien': ancien})
        
        # Password validation
        if len(new_pwd1) < 8:
            return render(request, 'comptes/changePassword.html', {'error': 'Le mot de passe doit contenir au moins 8 caractères'})
        if not re.search(r'[A-Z]', new_pwd1):
            return render(request, 'comptes/changePassword.html', {'error': 'Le mot de passe doit contenir au moins une lettre majuscule'})
        if not re.search(r'[a-z]', new_pwd1):
            return render(request, 'comptes/changePassword.html', {'error': 'Le mot de passe doit contenir au moins une lettre minuscule'})
        if not re.search(r'[0-9]', new_pwd1):
            return render(request, 'comptes/changePassword.html', {'error': 'Le mot de passe doit contenir au moins un chiffre'})
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_pwd1):
            return render(request, 'comptes/changePassword.html', {'error': 'Le mot de passe doit contenir au moins un caractère spécial'})
        
        request.user.set_password(new_pwd1)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return redirect('confirm_password')

    return render(request, 'comptes/changePassword.html')

#-----------------------------------------confirmation de changement de mot de passe---------------------------------------------#
class ConfirmationChange(LoginRequiredMixin,TemplateView):
    template_name = 'comptes/confirm_change.html'
    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['static_version'] = now().timestamp()
        return context

#-----------------------------------------Vue de confirmation de la creation ---------------------------------------------#
class ConfirmationCreat(TemplateView):
    template_name = 'comptes/confirm_creat.html'
    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['static_version'] = now().timestamp()
        return context
#-----------------------------------------Vue de profil---------------------------------------------#
@login_required
def profil_view(request):
    return render(request, 'comptes/profil.html',{'static_version': now().timestamp()})

#--------------------------------------------changement de photo de profil---------------------------------------------#
@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES['profile_picture']:
        profile_picture = request.FILES['profile_picture']
        fs = FileSystemStorage()
        filename = fs.save(profile_picture.name, profile_picture)
        uploaded_file_url = fs.url(filename)

        # Mettre à jour l'image de l'utilisateur

        request.user.image = filename
        request.user.save()

        messages.success(request, 'Photo de profil mise à jour avec succès.')
        return redirect('profil')

    return render(request, 'comptes/profil.html')

#--------------------------------------------changement de numéro de téléphone---------------------------------------------#
@login_required
def update_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Vérification du numéro de téléphone
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            messages.error(request, "Numéro de téléphone invalide.")
            return redirect('profil')

        # Mettre à jour le numéro de téléphone de l'utilisateur
        request.user.tel = phone_number
        request.user.save()

        messages.success(request, 'Numéro de téléphone mis à jour avec succès.')
        return redirect('profil')

    return render(request, 'comptes/profil.html',{'static_version': now().timestamp()})

#-----------------------------------------changement de l'email---------------------------------------------#
@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        password = request.POST.get('password')
        # Vérification du mot de passe
        if not request.user.check_password(password):
            message_password = "Mot de passe incorrect."
            return redirect('change_email')

        # Vérification de l'email
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', new_email):
            message_email= "Email invalide."
            return redirect('change_email')

        # Mettre à jour l'email de l'utilisateur
        request.user.email = new_email
        request.user.save()

        messages.success(request, 'Email mis à jour avec succès.')
        return redirect('confirm_email')

    return render(request, 'comptes/change_email.html',{'static_version': now().timestamp()})