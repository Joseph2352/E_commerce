from .models import Categorys

def categories_produits(request):
    categories = Categorys.objects.all()  # Récupérer toutes les catégories
    return {'categories_produits': categories}