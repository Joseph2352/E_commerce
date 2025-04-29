from django.db import models
from django.conf import settings


# Create your models here.
class Fournisseur(models.Model):
    logo = models.ImageField(upload_to='fournisseurs/logos/', blank=True, null=True)
    nom = models.CharField(max_length=255)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    abonnés = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='abonnements', blank=True)


    def __str__(self):
        return self.nom
    
    def nombre_abonnes(self):
        return self.abonnés.count()

    def taux_critiques_positives(self):
        total = self.critiques.count()
        positives = self.critiques.filter(note__gte=4).count()  # Exemple : note 4 ou 5
        if total == 0:
            return 0
        return round((positives / total) * 100, 1)

class Commentaire(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='critiques')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit = models.ForeignKey('produits.Produits', on_delete=models.CASCADE)
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    commentaire = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'produit')

