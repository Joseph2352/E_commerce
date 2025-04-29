from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Room)
class RootAdmin(admin.ModelAdmin):
    list_display=[
        "name",
    ]

admin.site.register(Message)