import random
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.timezone import now
from django.db.models import Max 

from produits.models import ProduitAime, Produits,Categorys,SuperCategorys

from django.contrib.auth.mixins import LoginRequiredMixin  # important si page protégée

def get_top_products_by_categories(category_slug):
    top_products = []

    for cat_slug in category_slug:
        try:
            # Récupère la catégorie par son nom
            category = Categorys.objects.get(slug=cat_slug)

            # Récupère le nombre max de likes dans cette catégorie
            max_likes = Produits.objects.filter(category=category).aggregate(Max('nombre_likes'))['nombre_likes__max']

            if max_likes is not None:
                # Récupère tous les produits ayant ce max de likes
                top_in_category = Produits.objects.filter(
                    category=category,
                    nombre_likes=max_likes
                )

                # Prend un au hasard s'il y a égalité
                selected_product = random.choice(list(top_in_category))
                top_products.append(selected_product)
            
        except Categorys.DoesNotExist:
            continue
    return top_products

class HomeViews(TemplateView):
    template_name = 'E_commerce/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Categorys.objects.all()
        context['categories_produits'] = {
            categorie: Produits.objects.filter(category=categorie)
            for categorie in categories
        }

        # ✅ Ajoute les produits aimés uniquement si l'utilisateur est connecté
        if self.request.user.is_authenticated:
            produits_aimes_ids = ProduitAime.objects.filter(
                utilisateur=self.request.user
            ).values_list('produit_id', flat=True)
            context['produits_aimes_ids'] = list(produits_aimes_ids)
        else:
            context['produits_aimes_ids'] = []

        categories_souhaitees = ["ordinateur", "tablettes-liseuses", "accessoires-informatique", "voiture", "motos", "velos"]
        produits_selectionnes = get_top_products_by_categories(categories_souhaitees)
        context['top_5_produits'] = produits_selectionnes
        context['static_version'] = now().timestamp()
        return context


def test(request):
    return render(request, 'E_commerce/test.html',{'static_version': now().timestamp()})

