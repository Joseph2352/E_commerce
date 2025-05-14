from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_room, name='chat_room'),
    path('room/<int:user_id>/', views.chat_room, name='chat_room'),
    path('send/', views.send_message, name='send_message'),
    path('upload/', views.upload_attachment, name='upload_attachment'),
    path('unread/', views.unread_ajax, name='unread_ajax'),
    path('messages/', views.messages_ajax, name='messages_ajax'),
    path('unread_count/', views.get_unread_count, name='unread_count'),
    path('delete_conversation/', views.delete_conversation, name='delete_conversation'),
    path('delete_message/', views.delete_message, name='delete_message'),
    path('edit_message/', views.edit_message, name='edit_message'),
    path('conversations_api/', views.conversations_api, name='conversations_api'),
    path('user_status/<int:user_id>/', views.user_status_api, name='user_status_api'),
]