from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils import timezone
from django.core.cache import cache
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Le super utilisateur doit avoir is_staff=True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Le super utilisateur doit avoir is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None  # désactiver le champ username
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(default=timezone.now)

    is_fournisseur = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def is_online(self):
        return cache.get(f"user_online_{self.id}") is True
