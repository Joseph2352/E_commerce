from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Fournisseur
from comptes.models import CustomUser


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
