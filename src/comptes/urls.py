from django.urls import path
from .views import ConfirmationCreat, change_email, changePassword, log_in,sign_up,profil_view, ConfirmationChange, update_phone_number, upload_profile_picture
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', log_in, name='login'),  
    path('singnup/',sign_up, name='singnup'),  
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profil/',profil_view,name='profil'),
    path('changepwd/', changePassword, name='changepwd' ),
    path('change_email/', change_email, name='change_email'),
    path('confirm_change/password', ConfirmationChange.as_view(title='Mot de passe'), name='confirm_password' ),
    path('confirm_change/email', ConfirmationChange.as_view(title='Email'), name='confirm_email' ),
    path('upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('update_phone_number/', update_phone_number, name='update_phone_number'),
    path('confirm_creat/compte', ConfirmationCreat.as_view(title='Compte'), name='confirm_creat_compte' ),
] 
