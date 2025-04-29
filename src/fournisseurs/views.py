from django.shortcuts import get_object_or_404, render,redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from fournisseurs.models import Fournisseur,Commentaire
from produits.models import Produits,Categorys,SuperCategorys


def EspaceFournisseur(request):
    return render(request ,"fournisseurs/spacefournisseur.html",{'static_version': now().timestamp()})

def boutique_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    produits = Produits.objects.filter(fournisseur=fournisseur)
    categories = Categorys.objects.all()
    supercategories = SuperCategorys.objects.all()

    search_query = request.GET.get('search', '')  

    produits = Produits.objects.filter(fournisseur=fournisseur)

    if search_query:
        produits = produits.filter(nom__icontains=search_query) | produits.filter(description__icontains=search_query)

    est_abonne = False

    if request.user.is_authenticated:
        est_abonne = fournisseur.abonnés.filter(id=request.user.id).exists()

    context = {
        'fournisseur': fournisseur,
        'produits': produits,
        'search_query': search_query,
        'est_abonne': est_abonne, 
        'categories': categories,
        'supercategories': supercategories,
        'active': 'accueil',
        'static_version': now().timestamp(),
    }
    return render(request, 'fournisseurs/boutique_fournisseur.html', context)

@login_required
def mes_produits(request):
    try:
        fournisseur = Fournisseur.objects.get(user=request.user)
        produits = Produits.objects.filter(fournisseur=fournisseur)
    except Fournisseur.DoesNotExist:
        produits = []  # L'utilisateur n'est pas un fournisseur

    return render(request, 'fournisseurs/mes_produits.html', {'produits': produits})

@login_required
def suivre_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    fournisseur.abonnés.add(request.user)
    return redirect('produits_par_fournisseur', fournisseur_id=fournisseur_id)


def Filter_Produit(request,fournisseur_id,filtersuper_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    supercategorie = get_object_or_404(SuperCategorys, id=filtersuper_id)
    categories_liees = Categorys.objects.filter(super_categorie=supercategorie)    
    produits = Produits.objects.filter(fournisseur=fournisseur, category__in=categories_liees)
    categories = Categorys.objects.all()
    supercategories = SuperCategorys.objects.all()

    search_query = request.GET.get('search', '')  

    if search_query:
        produits = produits.filter(nom__icontains=search_query) | produits.filter(description__icontains=search_query)

    est_abonne = False

    if request.user.is_authenticated:
        est_abonne = fournisseur.abonnés.filter(id=request.user.id).exists()

    context = {
        'fournisseur': fournisseur,
        'produits': produits,
        'search_query': search_query,
        'est_abonne': est_abonne, 
        'categories': categories,
        'supercategories': supercategories,
        'active': 'categories',
        'static_version': now().timestamp(),
    }
    return render(request, 'fournisseurs/Filterproduit.html', context)

@login_required
def laisser_commentaire(request, produit_id):
    produit = get_object_or_404(Produits, id=produit_id)
    fournisseur = produit.fournisseur

    if request.method == "POST":
        note = request.POST.get("note")
        commentaire = request.POST.get("commentaire")

        if note and commentaire:
            Commentaire.objects.create(
                fournisseur=fournisseur,
                utilisateur=request.user,
                produit=produit,
                note=int(note),
                commentaire=commentaire
            )
            return redirect("home")  # redirige vers une page de confirmation

    return render(request, "fournisseurs/commentaire.html", {"produit": produit, "fournisseur": fournisseur})



# def avis_view(request,fournisseur_id):
#     fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
#     commentaire = Commentaire.objects.filter(fournisseur=fournisseur)
#     return render(request, 'avis.html', {
#         'fournisseur': fournisseur,
#         'commentaire': commentaire,
#         'active': 'avis'
#     })

def avis_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
    commentaires = fournisseur.critiques.select_related('produit', 'utilisateur').order_by('-date')
    supercategories = SuperCategorys.objects.all()


    total = commentaires.count()
    positif = commentaires.filter(note__gte=4).count()
    neutre = commentaires.filter(note=3).count()
    negatif = commentaires.filter(note__lt=3).count()

    taux_positif = "{:.1f}".format((positif / total) * 100) if total > 0 else "0.0"
    taux_neutre = "{:.1f}".format((neutre / total) * 100) if total > 0 else "0.0"
    taux_negatif = "{:.1f}".format((negatif / total) * 100) if total > 0 else "0.0"

    context = {
        'fournisseur': fournisseur,
        'commentaires': commentaires,
        'supercategories': supercategories,
        'active': 'avis',
        'stats': {
            'total': total,
            'positif': positif,
            'neutre': neutre,
            'negatif': negatif,
            'taux_positif': taux_positif,
            'taux_neutre': taux_neutre,
            'taux_negatif': taux_negatif,
        },
        'static_version': now().timestamp(),
    }
    
    return render(request, 'fournisseurs/avis_fournisseur.html',context )

def produits_par_categorie(request, id):
    categorie = Categorys.objects.get(id=id)
    produits = Produits.objects.filter(categorie=categorie)
    categories = Categorys.objects.all()
    return render(request, 'categorie.html', {
        'categorie': categorie,
        'produits': produits,
        'categories': categories,
        'active': 'categories'
    })
