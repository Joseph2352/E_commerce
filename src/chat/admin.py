from django.contrib import admin
from .models import Conversation, Message, ChatAttachment

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'fournisseur', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('client__email', 'fournisseur__nom', 'firebase_chat_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'content', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp', 'sender')
    search_fields = ('content', 'sender__email', 'conversation__firebase_chat_id')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(ChatAttachment)
class ChatAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'file_type', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('conversation__firebase_chat_id', 'sender__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)





