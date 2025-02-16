from django.urls import path
from .views import log_in,sign_up,profil_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', log_in, name='login'),  
    path('singnup/',sign_up, name='singnup'),  
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profil/',profil_view,name='profil')
]
