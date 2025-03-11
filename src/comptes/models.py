from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("l'email est obligatoire")
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("le super utilisateur doit avoir is staff = True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("le super utilisateur doit avoir is superuser = True")
        
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True,blank=False)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
       # Ajoute des champs personnalisés à l'utilisateur
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"] 
    objects = MyUserManager ()

    def __str__(self):
        return self.email