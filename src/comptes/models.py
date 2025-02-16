from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # Ajoute des champs personnalisés à l'utilisateur
    first_name = None 
    last_name = None 
    fullname = models.CharField(max_length=40)
    date_joined = models.DateTimeField(auto_now_add=True)