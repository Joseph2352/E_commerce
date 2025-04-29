from django.contrib import admin

# Register your models here.
from produits.models import Categorys, Commande, CommandeProduit, Panier, ProduitAime,Produits,SuperCategorys,SousCategorys

@admin.register(SuperCategorys)
class SuperCategoryAdmin(admin.ModelAdmin):
    list_display=[
        "nom",
        "slug",
        "svg_icon",
    ]

@admin.register(Categorys)
class CategoryAdmin(admin.ModelAdmin):
    list_display=[
        "nom",
        "slug",
        "super_categorie",
    ]
    list_editable = ("slug",)

@admin.register(SousCategorys)
class SousCategoryAdmin(admin.ModelAdmin):
    list_display=[
        "nom",
        "slug",
        "categorie",
    ]

@admin.register(Produits)
class ProduitAdmin(admin.ModelAdmin):
    list_display=[
        "nom",
        "prix",
        "category",
        "sous_category",
        "nombre_likes",
        "date",

    ]

@admin.register(ProduitAime)
class ProduitAimeAdmin(admin.ModelAdmin):
    list_display=[
        "utilisateur",
        "produit",
        "date_ajout",
    ]

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display=[
        "user",
        "produit_id",
        "nom",
        "prix",
        "quantite",
        "date_ajout",
    ]
    
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display=[
        "user",
        "total",
        "date_commande",
    ]
    
@admin.register(CommandeProduit)
class CommandeProduitAdmin(admin.ModelAdmin):
    list_display=[
        "commande",
        "nom",
        "prix",
        "quantite",
    ]