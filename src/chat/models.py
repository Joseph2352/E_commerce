from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

def generate_unique_id():
    return str(uuid.uuid4())

class Conversation(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_client')
    fournisseur = models.ForeignKey('fournisseurs.Fournisseur', on_delete=models.CASCADE, related_name='conversations_fournisseur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    firebase_chat_id = models.CharField(max_length=255, unique=True, default=generate_unique_id)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat entre {self.client.email} et {self.fournisseur.nom}"

class ChatAttachment(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='attachments')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='chat_attachments/')
    file_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_image(self):
        return self.file_type.startswith('image/')

    def __str__(self):
        return f"Attachment from {self.sender} in {self.conversation}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_sent')
    content = models.TextField(default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    firebase_message_id = models.CharField(max_length=255, unique=True, default=generate_unique_id)
    attachment = models.ForeignKey(ChatAttachment, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message de {self.sender.email} à {self.timestamp}"


