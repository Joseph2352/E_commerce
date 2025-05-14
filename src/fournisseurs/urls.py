from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    avis_fournisseur, inscription_fournisseur,
    mes_produits, boutique_fournisseur, produits_par_categorie,
    suivre_fournisseur, Filter_Produit, laisser_commentaire,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
)
from . import views

app_name = 'fournisseurs'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('mes-produits/', views.mes_produits, name='mes_produits'),
    path('mes-produits/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('mes-produits/<int:produit_id>/editer/', views.editer_produit, name='editer_produit'),
    path('mes-produits/<int:produit_id>/supprimer/', views.supprimer_produit, name='supprimer_produit'),
    path('inscription-fournisseur/', inscription_fournisseur, name='inscription_fournisseur'),
    path('boutique-fournisseur/<int:fournisseur_id>/produits/',boutique_fournisseur, name='boutique_fournisseur'),
    path('fournisseur/<int:fournisseur_id>/suivre/', suivre_fournisseur, name='suivre_fournisseur'),
    path('categorie/<int:fournisseur_id>fournisseur/<int:filtersuper_id>categorie/', Filter_Produit, name='Filter_Produit'),
    path('<int:produit_id>/commentaire/', laisser_commentaire, name='laisser_commentaire'),
    path('fournisseur/<int:fournisseur_id>/avis/', avis_fournisseur, name='avis_fournisseur'),
    path('login/', views.login_fournisseur, name='login'),
    path('logout/', views.logout_fournisseur, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # URLs pour la réinitialisation du mot de passe
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]