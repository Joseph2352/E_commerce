from django import forms
from .models import Produits

class ProduitForm(forms.ModelForm):
    DEVISE_CHOICES = [
        ('EUR', 'Euro (€)'),
        ('USD', 'Dollar ($)'),
        ('XOF', 'Franc CFA (XOF)'),
        ('GBP', 'Livre (£)'),
        ('CAD', 'Dollar canadien (CAD)'),
        ('JPY', 'Yen (¥)'),
        ('CNY', 'Yuan (¥)'),
    ]

    devise = forms.ChoiceField(
        choices=DEVISE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Devise'
    )

    class Meta:
        model = Produits
        fields = ['nom', 'description', 'prix', 'devise', 'image', 'category']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control d-none',  # on cache le champ
                'id': 'customFileInput'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        } 