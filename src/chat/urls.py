from django.urls import path

from .views import  checkview, getMessages, home , room, send

urlpatterns = [
    path('', home , name ="chat_home"),
    path('<str:room>/', room , name ="room"),
    path('checkview', checkview , name ="checkview"),
    path('send', send , name ="send"),
    path('getMessages/<str:room>/', getMessages , name ="getMessages")

]