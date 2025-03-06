from django.urls import path
from django.views.generic import TemplateView

from .views import  PaymentConfirmationView, RechercheProduitView,HistoriqueRechercheView,ProduitViews,CheckoutView,ConfirmOrderView

urlpatterns = [
    path('recherche/',RechercheProduitView.as_view(), name='recherche'),
    path('historique/',HistoriqueRechercheView.as_view(), name='historique'),
    path("produits-<str:slug>/", ProduitViews.as_view(), name="produits"),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('confirm-order/', ConfirmOrderView.as_view(), name='confirm_order'),
    path('paiement-confirmation/<int:order_id>/', PaymentConfirmationView.as_view(), name='payment_confirmation'),
    path('order-confirmation/', TemplateView.as_view(template_name="produits/order_confirmation.html"), name='order_confirmation'), 
]