from django.contrib import admin

from .models import Fournisseur,Commentaire
# Register your models here.
@admin.register(Fournisseur)
class FornisseurAdmin(admin.ModelAdmin):
    list_display=[
        "user",
        "email",
        "nom",
        "telephone",
        "adresse",
        'logo',
    ]

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = [
        "fournisseur",
        "utilisateur",
        "produit",
        "note",
        "commentaire",
        "date",
    ]