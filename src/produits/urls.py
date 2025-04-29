from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('ajout_porduit',ajouter_produit, name='ajouter_produit'),
    path('recherche/',RechercheProduitView.as_view(), name='recherche'),
    path('favoris/', favoris, name='favoris'),
    path('favoris/toggle/<int:produit_id>/', toggle_favori, name='toggle_favori'),
    path('favoris/sync/', sync_favoris, name='sync_favoris'),    
    path('historique/',HistoriqueRechercheView.as_view(), name='historique'),
    path("produits-<str:slug>/", ProduitViews.as_view(), name="produits"),
    path('produit-<slug:super_categorie_slug>/', all_products, name='all_products'),
    path('test/', all_categories_and_products, name='test'),
    path('<int:id>-<str:nom>/', detail, name='produit_detail'), 
    path('checkout/', checkout, name='checkout'),    
    path('panier/', PanierView.as_view(), name='panier'),
    path('sync-panier/', sync_panier, name='sync_panier'),
    path('get_panier/', get_panier, name='get_panier'),
    path('commande/succes/', page_succes, name='page_succes'),
    
    # path('confirm-order/', ConfirmOrderView.as_view(), name='confirm_order'),
    # path('paiement-confirmation/<int:order_id>/', PaymentConfirmationView.as_view(), name='payment_confirmation'),
    path('order-confirmation/', TemplateView.as_view(template_name="produits/order_confirmation.html"), name='order_confirmation'), 
]