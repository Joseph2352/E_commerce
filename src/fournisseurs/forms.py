from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Fournisseur
from comptes.models import CustomUser
from django.contrib.auth import authenticate


class FournisseurSignupForm(UserCreationForm):
    last_name = forms.CharField(label="Nom",required=True)
    first_name = forms.CharField(label="Prenom",required=True)

    # Champs supplémentaires pour le fournisseur
    nom = forms.CharField(label="Nom de la boutique", required=True)
    logo = forms.ImageField(required=False)
    telephone = forms.CharField(label="Téléphone de la boutique", required=True)
    adresse = forms.CharField(required=False)
    description = forms.CharField(label='Description boutique',widget=forms.Textarea, required=True)
    
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "tel", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_fournisseur = True 
        if commit:
            user.save()
            
        # Créer le fournisseur lié
        Fournisseur.objects.create(
            user=user,
            nom=self.cleaned_data['nom'],
            logo=self.cleaned_data.get('logo'),
            adresse=self.cleaned_data.get('adresse'),
            telephone=self.cleaned_data.get('telephone'),
            description=self.cleaned_data.get('description'),
            email=user.email
        )

        return user

class FournisseurLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Votre mot de passe'})
    )
    remember_me = forms.BooleanField(required=False, label="Se souvenir de moi")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Email ou mot de passe incorrect.")
            if not user.is_fournisseur:
                raise forms.ValidationError("Ce compte n'est pas un compte fournisseur.")
            cleaned_data['user'] = user
        return cleaned_data
