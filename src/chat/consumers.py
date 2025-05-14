import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Conversation, Message
from fournisseurs.models import Fournisseur
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Abonnement au groupe personnel pour notifications
        user = self.scope["user"]
        if user.is_authenticated:
            await self.channel_layer.group_add(
                f'user_{user.id}',
                self.channel_name
            )
            cache.set(f"user_online_{user.id}", True, timeout=60)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        user = self.scope["user"]
        if user.is_authenticated:
            cache.delete(f"user_online_{user.id}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'chat_message':
            message = await self.save_message(data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )
        elif data['type'] == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing',
                    'user': data['user'],
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
        }))

    async def typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user'],
        }))

    async def new_conversation(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_conversation',
            'conversation': event['conversation'],
        }))

    @sync_to_async
    def save_message(self, data):
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
        except Conversation.DoesNotExist:
            sender = User.objects.get(id=data['sender_id'])
            if hasattr(sender, 'fournisseur'):
                fournisseur = sender.fournisseur
                client_id = data.get('other_user_id')
                client = User.objects.get(id=client_id)
            else:
                client = sender
                fournisseur = Fournisseur.objects.get(id=data.get('other_user_id'))
            conversation = Conversation.objects.create(client=client, fournisseur=fournisseur)
        user = User.objects.get(id=data['sender_id'])
        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            content=data['content']
        )
        # Avatar et initiale
        avatar = ''
        initial = ''
        if hasattr(user, 'image') and user.image:
            avatar = user.image.url
        elif hasattr(user, 'fournisseur') and hasattr(user.fournisseur, 'logo') and user.fournisseur.logo:
            avatar = user.fournisseur.logo.url
        if hasattr(user, 'first_name') and user.first_name:
            initial = user.first_name[0].upper()
        elif hasattr(user, 'fournisseur') and hasattr(user.fournisseur, 'nom') and user.fournisseur.nom:
            initial = user.fournisseur.nom[0].upper()
        return {
            'id': message.id,
            'sender_id': user.id,
            'sender_name': user.get_full_name() or user.email,
            'sender_avatar': avatar,
            'sender_initial': initial,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%H:%M'),
        } 