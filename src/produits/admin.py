from django.contrib import admin

# Register your models here.
from produits.models import Categorys,Produits

@admin.register(Categorys)
class CategoryAdmin(admin.ModelAdmin):
    list_display=[
        "nom",
        "slug",
    ]

@admin.register(Produits)
class ProduitAdmin(admin.ModelAdmin):
    list_display=[
        "nom",
        "prix",
        "category",
        "date",
    ]
