from django.contrib import admin

# Register your models here.
from .models import CustomUser

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display=[
        "fullname",
        "username",
        "email",
        "password",
    ]
