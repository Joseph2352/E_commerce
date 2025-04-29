from .models import Categorys,SuperCategorys

def categories_produits(request):
    categories = Categorys.objects.all()  # Récupérer toutes les catégories
    return {'categories_produits': categories}

def super_categories(request):
    return {'super_categories': SuperCategorys.objects.all()}