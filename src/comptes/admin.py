from django.contrib import admin

# Register your models here.
from .models import CustomUser

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display=[
        "first_name",
        "last_name",
        "email",
        "tel",
        "password",
        "image",
    ]
