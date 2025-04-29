from django.urls import path
from .views import EspaceFournisseur, avis_fournisseur,mes_produits,boutique_fournisseur, produits_par_categorie, suivre_fournisseur,Filter_Produit,laisser_commentaire


urlpatterns = [
    # path('', EspaceFournisseur , name = 'espace_fournisseur'),
    # path('mes-produits/', mes_produits, name='mes_produits'),
    path('<int:fournisseur_id>/produits/',boutique_fournisseur, name='produits_par_fournisseur'),
    path('fournisseur/<int:fournisseur_id>/suivre/', suivre_fournisseur, name='suivre_fournisseur'),
    path('categorie/<int:fournisseur_id>fournisseur/<int:filtersuper_id>categorie/', Filter_Produit, name='Filter_Produit'),
    path('<int:produit_id>/commentaire/', laisser_commentaire, name='laisser_commentaire'),
    path('fournisseur/<int:fournisseur_id>/avis/', avis_fournisseur, name='avis_fournisseur'),


]