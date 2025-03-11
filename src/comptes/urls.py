from django.urls import path
from .views import change_email, changePassword, log_in,sign_up,profil_view, ConfirmationChange, update_phone_number, upload_profile_picture
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', log_in, name='login'),  
    path('singnup/',sign_up, name='singnup'),  
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profil/',profil_view,name='profil'),
    path('changepwd/', changePassword, name='changepwd' ),
    path('change_email/', change_email, name='change_email'),
    path('confirmation_change/password', ConfirmationChange.as_view(title='mot de passe'), name='confirmation_password' ),
    path('confirmation_change/email', ConfirmationChange.as_view(title='Email'), name='confirmation_email' ),
    path('upload_profile_picture/', upload_profile_picture, name='upload_profile_picture'),
    path('update_phone_number/', update_phone_number, name='update_phone_number'),

] 
