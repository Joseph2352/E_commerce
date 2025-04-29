from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import F, Exists, OuterRef


from produits.models import *




from io import BytesIO
from PIL import Image
import base64
import os
from django.core.files.base import ContentFile
from django.conf import settings

def ajouter_produit(request):
    categories = Categorys.objects.all().order_by('nom')

    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        prix = request.POST.get('prix')
        categorie_id = request.POST.get('category')
        image = request.FILES.get('image')  # Image originale

        # Image recadrée depuis le formulaire
        cropped_image_data = request.POST.get('cropped_image')  # Image recadrée en base64
        if cropped_image_data:
            format, imgstr = cropped_image_data.split(';base64,')  # Extraire le format et l'image
            ext = format.split('/')[1]  # Récupérer l'extension (jpg, png, etc.)
            imgdata = base64.b64decode(imgstr)  # Décoder l'image base64
            image_file = BytesIO(imgdata)
            image = Image.open(image_file)  # Ouvrir l'image avec PIL

            # Créer le fichier temporaire pour l'image recadrée
            image_name = f"cropped_image.{ext}"
            image_path = os.path.join(settings.MEDIA_ROOT, 'image_Produit', image_name)

            # Créer le répertoire si nécessaire
            os.makedirs(os.path.dirname(image_path), exist_ok=True)

            # Sauvegarder l'image recadrée
            image.save(image_path)

            # Utiliser le fichier d'image sauvegardé pour l'objet ImageField
            with open(image_path, 'rb') as img_file:
                django_image = ContentFile(img_file.read(), name=image_name)
                produit_image = django_image

        else:
            # Si l'image recadrée n'est pas présente, utiliser l'image téléchargée
            produit_image = image

        # Vérification des champs obligatoires
        if not nom or not description or not prix or not categorie_id:
            messages.error(request, "Tous les champs sont obligatoires.")
        else:
            try:
                # Récupérer la catégorie choisie
                categorie = Categorys.objects.get(id=categorie_id)

                # Créer le produit dans la base de données
                produit = Produits.objects.create(
                    nom=nom,
                    description=description,
                    prix=prix,
                    category=categorie,
                    image=produit_image  # Lien vers l'image téléchargée
                )
                messages.success(request, f"Le produit '{produit.nom}' a été ajouté avec succès.")
                return redirect('ajouter_produit')  # Rediriger après succès
            except Categorys.DoesNotExist:
                messages.error(request, "La catégorie choisie n'existe pas.")

    # Renvoyer la vue avec les catégories
    return render(request, 'produits/formulaire_ajout_produit.html', {'categories': categories})


@login_required
@require_POST
def toggle_favori(request, produit_id):
    try:
        # Vérifie d'abord si le produit existe
        produit = Produits.objects.get(id=produit_id)
        
        with transaction.atomic():
            # Vérifie si l'utilisateur a déjà liké ce produit
            favori = ProduitAime.objects.filter(
                utilisateur=request.user,
                produit=produit
            ).first()
            
            if favori:
                # Dislike - supprime le like
                favori.delete()
                # Met à jour le compteur (en s'assurant qu'il ne devient pas négatif)
                Produits.objects.filter(
                    id=produit_id,
                    nombre_likes__gt=0  # Seulement si le compteur > 0
                ).update(
                    nombre_likes=F('nombre_likes') - 1
                )
                liked = False
            else:
                # Like - ajoute un nouveau like
                ProduitAime.objects.create(
                    utilisateur=request.user,
                    produit=produit
                )
                # Incrémente le compteur
                Produits.objects.filter(id=produit_id).update(
                    nombre_likes=F('nombre_likes') + 1
                )
                liked = True
            
            # Rafraîchit les données du produit
            produit.refresh_from_db()
            
            return JsonResponse({
                'liked': liked,
                'total_likes': produit.nombre_likes,
                'produit_id': produit.id
            })
            
    except Produits.DoesNotExist:
        return JsonResponse({'error': 'Produit non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)  
    
@login_required
@require_POST
def sync_favoris(request):
    try:
        data = json.loads(request.body)
        favoris = data.get('favoris', [])
        
        for fav in favoris:
            produit = Produits.objects.get(id=fav['id'])
            ProduitAime.objects.get_or_create(
                utilisateur=request.user,
                produit=produit
            )
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
@login_required
def favoris(request):
    produits_aimes = Produits.objects.filter(
        produitaime__utilisateur=request.user
    ).distinct()
    
    return render(request, 'produits/favoris.html', {
        'produits_aimes': produits_aimes,
        'static_version': now().timestamp()
    })

    
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
    assert produit.fournisseur is not None, "Ce produit n’a pas de fournisseur."
    return render(request, 'produits/detail.html', {'produit': produit,'static_version': now().timestamp()})

class PanierView(TemplateView):
    template_name = "produits/panier.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["static_version"] = now().timestamp()  
        return context



@login_required
def sync_panier(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cart = data.get('cart', [])

            panier_existant = {item.produit_id: item for item in Panier.objects.filter(user=request.user)}

            # Liste des IDs présents dans le panier actuel (côté navigateur)
            produits_dans_panier = set()

            for item in cart:
                produit_id = int(item.get('id'))
                produits_dans_panier.add(produit_id)

                nom = item.get('nom')
                prix = item.get('prix')
                quantite = item.get('quantite', 1)
                image = item.get('image')

                if produit_id in panier_existant:
                    # Mettre à jour
                    panier_item = panier_existant[produit_id]
                    panier_item.nom = nom
                    panier_item.prix = prix
                    panier_item.quantite = quantite
                    panier_item.image = image
                    panier_item.save()
                else:
                    # Créer un nouveau
                    Panier.objects.create(
                        user=request.user,
                        produit_id=produit_id,
                        nom=nom,
                        prix=prix,
                        quantite=quantite,
                        image=image
                    )

            # ⚡ Supprimer les produits qui ne sont plus dans le panier local
            for produit_id, panier_item in panier_existant.items():
                if produit_id not in produits_dans_panier:
                    panier_item.delete()

            return JsonResponse({"message": "Panier synchronisé avec succès."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Méthode non autorisée."}, status=405)

@login_required
def get_panier(request):
    panier_items = Panier.objects.filter(user=request.user)
    panier_data = []

    for item in panier_items:
        panier_data.append({
            "id": item.produit_id,
            "nom": item.nom,
            "prix": float(item.prix),  # convertir en float pour JS
            "quantite": item.quantite,
            "image": item.image,
        })

    return JsonResponse({"panier": panier_data})

# class ConfirmOrderView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         try:
#             data = json.loads(request.body)  
#             logger.info(f"🚀 Données reçues : {data}")

#             cart = data.get('cart', [])
#             if not cart:
#                 return JsonResponse({'error': 'Votre panier est vide !'}, status=400)

#             product_ids = [produit.get('id') for produit in cart]
#             products = Produits.objects.filter(id__in=product_ids)

#             if not products.exists():
#                 return JsonResponse({'error': 'Certains produits ne sont pas disponibles !'}, status=400)

#             total_price = sum(product.prix * int(produit.get('quantite', 1))
#                               for produit in cart
#                               for product in products if product.id == produit.get('id'))

#             # Créer la commande
#             order = Order.objects.create(user=request.user, total_price=total_price)

#             # Générer un lien de paiement avec Paycard
#             paycard_url = self.generer_lien_paycard(order)

#             return JsonResponse({'message': 'Commande validée !', 'payment_url': paycard_url})

#         except json.JSONDecodeError:
#             logger.error("❌ Erreur JSON : Données mal formatées")
#             return JsonResponse({'error': 'Données mal formatées'}, status=400)
#         except Exception as e:
#             logger.error(f"❌ Erreur : {str(e)}")
#             return JsonResponse({'error': str(e)}, status=400)

#     def generer_lien_paycard(self, order):
#         """
#         Envoie une requête à l'API Paycard pour générer un lien de paiement.
#         """
#         url_api_paycard = "https://api.paycard.com/payment"
#         payload = {
#             "amount": str(order.total_price),
#             "currency": "EUR",
#             "order_id": str(order.id),
#             "return_url": f"{settings.SITE_URL}/produit/paiement-confirmation/{order.id}/",
#             "cancel_url": f"{settings.SITE_URL}/produit/paiement-annule/{order.id}/",
#             "customer_email": order.user.email
#         }

#         headers = {
#             "Authorization": f"Bearer {settings.PAYCARD_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         response = requests.post(url_api_paycard, json=payload, headers=headers)

#         if response.status_code == 200:
#             return response.json().get("payment_url")
#         else:
#             logger.error(f"Erreur Paycard: {response.text}")
#             return None
        
# class PaymentConfirmationView(LoginRequiredMixin, View):
#     def get(self, request, order_id, *args, **kwargs):
#         try:
#             order = Order.objects.get(id=order_id, user=request.user)

#             # Marquer la commande comme "payée"
#             order.status = "payé"
#             order.save()

#             return JsonResponse({'message': 'Paiement validé !', 'order_id': order.id})
#         except Order.DoesNotExist:
#             return JsonResponse({'error': 'Commande introuvable !'}, status=404)

# views.py


@login_required
def checkout(request):
    if request.method == "POST":
        produits_data = []
        index = 0

        while True:
            nom = request.POST.get(f'produits[{index}][nom]')
            prix = request.POST.get(f'produits[{index}][prix]')
            quantite = request.POST.get(f'produits[{index}][quantite]')
            
            if nom is None:
                break

            # Correction: gérer la virgule dans les prix
            if prix is not None:
                prix = prix.replace(',', '.')
                try:
                    prix = float(prix)
                except ValueError:
                    return JsonResponse({'success': False, 'error': f"Prix invalide pour le produit {nom}."})

            # Correction: vérification de la quantité aussi
            try:
                quantite = int(quantite)
            except (ValueError, TypeError):
                quantite = 1  # Valeur par défaut

            produits_data.append({
                'nom': nom,
                'prix': prix,
                'quantite': quantite
            })
            index += 1

        if not produits_data:
            return JsonResponse({'success': False, 'error': 'Aucun produit trouvé.'})

        # Créer la commande
        total = sum(p['prix'] * p['quantite'] for p in produits_data)
        commande = Commande.objects.create(user=request.user, total=total)

        # Ajouter chaque produit
        for produit in produits_data:
            CommandeProduit.objects.create(
                commande=commande,
                nom=produit['nom'],
                prix=produit['prix'],
                quantite=produit['quantite']
            )

        return redirect('page_succes')

    else:
        return render(request, 'produits/checkout.html', {'static_version': now().timestamp()})
    
@login_required
def page_succes(request):
    return render(request, 'produits/page_succes.html')

#---------------------Tous les produits d'une super categorie ----------------------------------------
def all_products(request, super_categorie_slug):
    super_categorie = get_object_or_404(SuperCategorys, slug=super_categorie_slug)
    produits_list = Produits.objects.filter(category__super_categorie__slug=super_categorie_slug)
    
    paginator = Paginator(produits_list, 15)  # 15 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)
    
    context = {
        'produits': produits,
        'super_categorie': super_categorie,
        'static_version': now().timestamp(),
    }
    return render(request, 'produits/all_produit_super_categorie.html', context)

def all_categories_and_products(request):
    super_categories = SuperCategorys.objects.all()
    categories = Categorys.objects.all()
    sous_categories = SousCategorys.objects.all()
    produits = Produits.objects.all()
    print("Super Categories:", super_categories)
    print("Categories:", categories)
    print("Sous Categories:", sous_categories)
    print("Produits:", produits)
    context = {
        'super_categories': super_categories,
        'categories': categories,
        'sous_categories': sous_categories,
        'produits': produits,
    }
    return render(request, 'produits/test.html', context)

