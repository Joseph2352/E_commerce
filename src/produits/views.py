from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from django.http import JsonResponse
import json

from produits.models import Produits,Categorys,RechercheUtilisateur,Order


# Create your views here.
class RechercheProduitView(ListView):
    model = Produits
    template_name = 'produits/recherche.html'
    context_object_name = 'produits'

    def get_queryset(self):
        recherche_term = self.request.GET.get('recherche', '').strip()
        if recherche_term:
            produits = Produits.objects.filter(nom__icontains=recherche_term)

            # Sauvegarde la recherche de l'utilisateur connecté
            if self.request.user.is_authenticated:
                RechercheUtilisateur.objects.create(
                    utilisateur=self.request.user,
                    terme=recherche_term
                )
            return produits
        return Produits.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['static_version'] = now().timestamp()
        return context
    
class HistoriqueRechercheView(LoginRequiredMixin, ListView):
    model = RechercheUtilisateur
    template_name = 'produits/historique.html'
    context_object_name = 'recherches'

    def get_queryset(self):
        return RechercheUtilisateur.objects.filter(utilisateur=self.request.user).order_by('-date_recherche')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['static_version'] = now().timestamp()
        return context

class ProduitViews(ListView):
    model = Produits  # Définit le modèle principal
    template_name = "produits/produit.html"
    context_object_name = "categorie"

    def get_queryset(self):
        """ Récupère les produits d'une catégorie spécifique. """
        self.category = get_object_or_404(Categorys, nom=self.kwargs.get("nom_category"))
        return Produits.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        """ Ajoute des données supplémentaires au contexte. """
        context = super().get_context_data(**kwargs)
        context["category"] = self.category  # Ajout de la catégorie actuelle
        context["static_version"] = now().timestamp()  # Version statique
        return context
    
class CheckoutView(TemplateView):
    template_name = "produits/checkout.html"


class ConfirmOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)  # Lire le corps de la requête
            cart = data.get('cart', [])

            if not cart:
                return JsonResponse({'error': 'Votre panier est vide !'}, status=400)

            # Extraire les IDs des produits à partir de la liste 'cart'
            product_ids = [produit['id'] for produit in cart]

            # Récupérer les produits avec les IDs
            products = Produits.objects.filter(id__in=product_ids)

            # Calculer le prix total
            total_price = 0
            for produit in cart:
                product = next((p for p in products if p.id == produit['id']), None)
                if product:
                    # Assumons une quantité de 1 pour chaque produit
                    total_price += product.prix

            # Créer la commande
            order = Order.objects.create(user=request.user, total_price=total_price)
            order.products.set(products)

            # Vider le panier après la commande
            request.session['cart'] = []

            return JsonResponse({'message': 'Commande validée !', 'redirect_url': reverse('order_confirmation')})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données mal formatées'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
