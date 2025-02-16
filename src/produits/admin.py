from django.contrib import admin

# Register your models here.
from produits.models import Categorys,Produits,SuperCategorys,SousCategorys

@admin.register(SuperCategorys)
class SuperCategoryAdmin(admin.ModelAdmin):
    list_display=[
        "nom",
        "slug",
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
        "date",
    ]
