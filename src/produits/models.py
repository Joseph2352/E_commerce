from django.conf import settings
from django.db import models
from django.utils.text import  slugify
from django.contrib.auth.models import User

from fournisseurs.models import Fournisseur

# Create your models here.
class SuperCategorys(models.Model):
    nom = models.CharField(max_length=40)
    image = models.ImageField(upload_to='image_super_Category')
    slug = models.SlugField(blank=True, null=True, unique=True)
    svg_icon = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = '1-Super Categorie'
    
    def __str__(self):
        return self.nom
    
    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug= slugify(self.nom)  #permet de convertir une chaine de caractère en slug

        super().save(*args, **kwargs)
    
class Categorys(models.Model):
    nom = models.CharField(max_length=40)
    description = models.TextField()
    super_categorie = models.ForeignKey(SuperCategorys,on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True, unique=True)
    class Meta:
        verbose_name = '2-Categorie'

    def __str__(self):
        return self.nom
    
    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug= slugify(self.nom)  #permet de convertir une chaine de caractère en slug

        super().save(*args, **kwargs)
    
class SousCategorys(models.Model):
    nom = models.CharField(max_length=40)
    categorie = models.ForeignKey(Categorys,on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True, unique=True)
    class Meta:
        verbose_name = '3-Sous Categorie'

    def __str__(self):
        return self.nom
    
    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug= slugify(self.nom)  #permet de convertir une chaine de caractère en slug

        super().save(*args, **kwargs)
    
class Produits(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='image_Produit')
    date = models.DateField(auto_now=True)
    prix = models.FloatField()
    category = models.ForeignKey(Categorys,on_delete=models.CASCADE)
    sous_category = models.ForeignKey(SousCategorys,on_delete=models.CASCADE,null=True,blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    nombre_likes = models.PositiveIntegerField(default=0, verbose_name="Nombre de likes")

    class Meta:
        verbose_name = 'Produit'
        ordering = ['-date']
    
    def __str__(self):
        return self.nom

class ProduitAime(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('utilisateur', 'produit')  # Empêche les doublons
        verbose_name = 'Produit aimé'
        ordering = ['-date_ajout']
    
    def __str__(self):
        return f"{self.utilisateur.username} aime {self.produit.nom}"
    
class RechercheUtilisateur(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    terme = models.CharField(max_length=200)
    date_recherche = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Utilisateur} - {self.termes} - {self.date_recherche}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Produits)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.id} - {self.user.email}"

class Panier(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit_id = models.IntegerField()
    nom = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500)
    quantite = models.PositiveIntegerField(default=1)  # Si tu veux gérer les quantités plus tard
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.user.email}"
    
class Commande(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande #{self.id} de {self.user.email}"

class CommandeProduit(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='produits')
    nom = models.CharField(max_length=255)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.nom} (x{self.quantite})"