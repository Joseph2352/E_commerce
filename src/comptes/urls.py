from django.urls import path
from .views import log_in,sign_up

urlpatterns = [
    path('login/', log_in, name='login'),  
    path('singnup/',sign_up, name='singnup'),  
]
