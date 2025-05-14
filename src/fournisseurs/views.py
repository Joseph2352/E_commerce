from django.shortcuts import get_object_or_404, render,redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from fournisseurs.models import Fournisseur,Commentaire
from produits.models import Produits,Categorys,SuperCategorys
from django.shortcuts import render, redirect
from .forms import FournisseurSignupForm, FournisseurLoginForm

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
    print(f"Utilisateur connecté : {request.user}")
    fournisseur = get_object_or_404(Fournisseur, user=request.user)
    print(f"Fournisseur trouvé : {fournisseur}")
    produits_list = Produits.objects.filter(fournisseur=fournisseur)
    print(f"Nombre de produits trouvés : {produits_list.count()}")
    categories = Categorys.objects.all()
    supercategories = SuperCategorys.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        produits_list = produits_list.filter(nom__icontains=search_query) | produits_list.filter(description__icontains=search_query)
        print(f"Nombre de produits après recherche : {produits_list.count()}")

    paginator = Paginator(produits_list, 8)  # 8 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)
    print(f"Page actuelle : {produits.number}, Nombre total de pages : {produits.paginator.num_pages}")

    context = {
        'fournisseur': fournisseur,
        'produits': produits,
        'search_query': search_query,
        'categories': categories,
        'supercategories': supercategories,
        'active': 'mes_produits',
        'static_version': now().timestamp(),
    }
    return render(request, 'fournisseurs/mes_produits.html', context)

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


def inscription_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurSignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte fournisseur a été créé avec succès !")
            return redirect('login')  # Ou vers une autre page
    else:
        form = FournisseurSignupForm()

    return render(request, 'fournisseurs/inscription_fournisseur.html', {'form': form})


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

def login_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            messages.success(request, 'Connexion réussie !')
            return redirect('fournisseurs:dashboard')
        # Les erreurs sont déjà gérées par le formulaire
    else:
        form = FournisseurLoginForm()
    return render(request, 'fournisseurs/login_fournisseur.html', {'form': form})

@login_required
def dashboard(request):
    if not request.user.is_fournisseur:
        messages.error(request, 'Accès non autorisé.')
        return redirect('home')
    
    fournisseur = request.user.fournisseur
    context = {
        'fournisseur': fournisseur,
    }
    return render(request, 'fournisseurs/dashboard.html', context)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'fournisseurs/password_reset_form.html'
    email_template_name = 'fournisseurs/password_reset_email.html'
    subject_template_name = 'fournisseurs/password_reset_subject.txt'
    success_url = reverse_lazy('fournisseurs:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'fournisseurs/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'fournisseurs/password_reset_confirm.html'
    success_url = reverse_lazy('fournisseurs:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'fournisseurs/password_reset_complete.html'

@login_required
def ajouter_produit(request):
    from produits.models import Produits
    from produits.forms import ProduitForm  # À créer si non existant
    fournisseur = get_object_or_404(Fournisseur, user=request.user)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            produit.fournisseur = fournisseur
            produit.save()
            messages.success(request, 'Produit ajouté avec succès !')
            return redirect('fournisseurs:mes_produits')
    else:
        form = ProduitForm()
    return render(request, 'fournisseurs/ajouter_produit.html', {'form': form})

@login_required
def editer_produit(request, produit_id):
    from produits.models import Produits
    from produits.forms import ProduitForm
    fournisseur = get_object_or_404(Fournisseur, user=request.user)
    produit = get_object_or_404(Produits, id=produit_id, fournisseur=fournisseur)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produit modifié avec succès !')
            return redirect('fournisseurs:mes_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'fournisseurs/editer_produit.html', {'form': form, 'produit': produit})

@login_required
def supprimer_produit(request, produit_id):
    from produits.models import Produits
    fournisseur = get_object_or_404(Fournisseur, user=request.user)
    produit = get_object_or_404(Produits, id=produit_id, fournisseur=fournisseur)
    if request.method == 'POST':
        produit.delete()
        messages.success(request, 'Produit supprimé avec succès !')
        return redirect('fournisseurs:mes_produits')
    return render(request, 'fournisseurs/supprimer_produit.html', {'produit': produit})

def logout_fournisseur(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('fournisseurs:login')

