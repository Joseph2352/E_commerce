from django.contrib import admin

from .models import Fournisseur,Commentaire
# Register your models here.
@admin.register(Fournisseur)
class FornisseurAdmin(admin.ModelAdmin):
    list_display=[
        "nom",
        "telephone",
        "adresse",
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