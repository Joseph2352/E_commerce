from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
import json
import requests 
from django.http import JsonResponse
from django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.conf import settings
import logging

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
        self.category = get_object_or_404(Categorys, slug=self.kwargs.get("slug"))
        return Produits.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        """ Ajoute des données supplémentaires au contexte. """
        context = super().get_context_data(**kwargs)
        context["category"] = self.category  # Ajout de la catégorie actuelle
        context["static_version"] = now().timestamp()  # Version statique
        return context

def detail(request, id , nom):
    produit = get_object_or_404(Produits, pk=id)
    return render(request, 'produits/detail.html', {'produit': produit})

class CheckoutView(TemplateView):
    template_name = "produits/checkout.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["static_version"] = now().timestamp()  
        return context


logger = logging.getLogger(__name__)  # Logger pour voir les erreurs

class ConfirmOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)  
            logger.info(f"🚀 Données reçues : {data}")

            cart = data.get('cart', [])
            if not cart:
                return JsonResponse({'error': 'Votre panier est vide !'}, status=400)

            product_ids = [produit.get('id') for produit in cart]
            products = Produits.objects.filter(id__in=product_ids)

            if not products.exists():
                return JsonResponse({'error': 'Certains produits ne sont pas disponibles !'}, status=400)

            total_price = sum(product.prix * int(produit.get('quantite', 1))
                              for produit in cart
                              for product in products if product.id == produit.get('id'))

            # Créer la commande
            order = Order.objects.create(user=request.user, total_price=total_price)

            # Générer un lien de paiement avec Paycard
            paycard_url = self.generer_lien_paycard(order)

            return JsonResponse({'message': 'Commande validée !', 'payment_url': paycard_url})

        except json.JSONDecodeError:
            logger.error("❌ Erreur JSON : Données mal formatées")
            return JsonResponse({'error': 'Données mal formatées'}, status=400)
        except Exception as e:
            logger.error(f"❌ Erreur : {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    def generer_lien_paycard(self, order):
        """
        Envoie une requête à l'API Paycard pour générer un lien de paiement.
        """
        url_api_paycard = "https://api.paycard.com/payment"
        payload = {
            "amount": str(order.total_price),
            "currency": "EUR",
            "order_id": str(order.id),
            "return_url": f"{settings.SITE_URL}/produit/paiement-confirmation/{order.id}/",
            "cancel_url": f"{settings.SITE_URL}/produit/paiement-annule/{order.id}/",
            "customer_email": order.user.email
        }

        headers = {
            "Authorization": f"Bearer {settings.PAYCARD_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(url_api_paycard, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json().get("payment_url")
        else:
            logger.error(f"Erreur Paycard: {response.text}")
            return None
        
class PaymentConfirmationView(LoginRequiredMixin, View):
    def get(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id, user=request.user)

            # Marquer la commande comme "payée"
            order.status = "payé"
            order.save()

            return JsonResponse({'message': 'Paiement validé !', 'order_id': order.id})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Commande introuvable !'}, status=404)



#---------------------Tous les produits d'une super categorie ----------------------------------------
def all_products(request, super_categorie_slug):
    super_categorie = get_object_or_404(Categorys, slug=super_categorie_slug)
    produits = Produits.objects.filter(category__super_categorie__slug=super_categorie_slug)
    context = {
        'produits': produits,
        'super_categorie': super_categorie,
        'static_version': now().timestamp(),
    }
    return render(request, 'produits/all_produit_super_categorie.html', context)