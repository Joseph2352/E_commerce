from django.conf import settings
from django.db import models
from django.utils.text import  slugify
from django.contrib.auth.models import User

# Create your models here.
class SuperCategorys(models.Model):
    nom = models.CharField(max_length=40)
    image = models.ImageField(upload_to='image_super_Category')
    slug = models.SlugField(blank=True, null=True, unique=True)

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
    category = models.ForeignKey(Categorys,on_delete=models.CASCADE,related_name='main_categories')
    sous_category = models.ForeignKey(Categorys,on_delete=models.CASCADE,null=True,blank=True,related_name='sub_categories')

    class Meta:
        verbose_name = 'Produit'
        ordering = ['-date']
    
    def __str__(self):
        return self.nom
    
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
        return f"Commande {self.id} - {self.user.username}"