from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now
from .models import Conversation, Message, ChatAttachment
from fournisseurs.models import Fournisseur
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.exceptions import PermissionDenied
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.timesince import timesince


@login_required
def chat_room(request, user_id=None):
    if user_id is None:
        # Afficher la liste des conversations SANS conversation sélectionnée
        if hasattr(request.user, 'is_fournisseur') and request.user.is_fournisseur:
            conversations = Conversation.objects.filter(fournisseur__user=request.user).order_by('-updated_at')
            template = "fournisseurs/base_fournisseur.html"
        else:
            conversations = Conversation.objects.filter(client=request.user).order_by('-updated_at')
            template = "E_commerce/base1.html"
        return render(request, 'chat/chat_home.html', {
            'conversations': conversations,
             'template': template,
            'static_version': now().timestamp(),
        })

    User = get_user_model()
    if hasattr(request.user, 'is_fournisseur') and request.user.is_fournisseur:
        # L'ID dans l'URL est celui du client
        client = get_object_or_404(User, id=user_id)
        fournisseur = request.user.fournisseur
        template = "fournisseurs/base_fournisseur.html"
        print(template)
    else:
        # L'ID dans l'URL est celui du fournisseur
        fournisseur = get_object_or_404(Fournisseur, id=user_id)
        client = request.user
        template = "E_commerce/base1.html"
        print(template)

    conversation_id = request.GET.get('conversation_id')

    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if request.user != conversation.client and request.user != conversation.fournisseur.user:
            raise PermissionDenied
    else:
        conversation = Conversation.objects.filter(client=client, fournisseur=fournisseur).first()
        conversation_was_existing = bool(conversation)
        if not conversation:
            conversation = Conversation.objects.create(client=client, fournisseur=fournisseur)
        # Diffusion WebSocket si nouvelle conversation
        if not conversation_was_existing:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{fournisseur.user.id}',
                {
                    'type': 'new_conversation',
                    'conversation': {
                        'id': conversation.id,
                        'client_name': client.get_full_name() or client.email,
                        'client_avatar': client.image.url if hasattr(client, 'image') and client.image else '',
                        'last_message': '',
                        'last_message_time': '',
                    }
                }
            )

    messages = Message.objects.filter(conversation=conversation).order_by('timestamp') if conversation else []
    if conversation:
        Message.objects.filter(conversation=conversation, is_read=False).exclude(sender=request.user).update(is_read=True)

    # Rafraîchir la liste des conversations après le markAsRead
    if hasattr(request.user, 'is_fournisseur') and request.user.is_fournisseur:
        conversations = Conversation.objects.filter(fournisseur__user=request.user).order_by('-updated_at')
    else:
        conversations = Conversation.objects.filter(client=request.user).order_by('-updated_at')

    context = {
        'conversation': conversation,
        'messages': messages,
        'fournisseur': fournisseur,
        'other_user': client,
        'conversations': conversations,
        'template': template,
        'show_list': False,
        'static_version': now().timestamp(),
    }
    return render(request, 'chat/chat_room.html', context)

@login_required
@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        conversation_id = data.get('conversation_id')
        content = data.get('content')
        client = request.user
        fournisseur = None
        if hasattr(request.user, 'is_fournisseur') and request.user.is_fournisseur:
            fournisseur = request.user.fournisseur
            client_id = data.get('other_user_id')
            if client_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                client = User.objects.get(id=client_id)
        else:
            fournisseur_id = data.get('other_user_id')
            if fournisseur_id:
                fournisseur = Fournisseur.objects.get(id=fournisseur_id)
        conversation = None
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
        else:
            # Crée la conversation ici si elle n'existe pas
            conversation = Conversation.objects.filter(client=client, fournisseur=fournisseur).first()
            if not conversation:
                conversation = Conversation.objects.create(client=client, fournisseur=fournisseur)
        # Vérifier si l'utilisateur est le client ou le fournisseur de la conversation
        if request.user != conversation.client and request.user != conversation.fournisseur.user:
            raise PermissionDenied
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        return JsonResponse({
            'status': 'success',
            'message_id': message.id,
            'conversation_id': conversation.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_http_methods(["POST"])
def upload_attachment(request):
    try:
        file = request.FILES.get('file')
        conversation_id = request.POST.get('conversation_id')
        description = request.POST.get('description', '')
        
        if not file:
            return JsonResponse({'status': 'error', 'message': 'No file provided'}, status=400)
            
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if request.user != conversation.client and request.user != conversation.fournisseur.user:
            raise PermissionDenied
            
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'chat_attachments', str(conversation_id))
        os.makedirs(upload_dir, exist_ok=True)
        filename = f"{int(timezone.now().timestamp())}_{file.name}"
        file_path = os.path.join('chat_attachments', str(conversation_id), filename)
        path = default_storage.save(file_path, ContentFile(file.read()))
        
        attachment = ChatAttachment.objects.create(
            conversation=conversation,
            sender=request.user,
            file=path,
            file_type=file.content_type,
            description=description
        )
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=description or "Pièce jointe",
            attachment=attachment
        )
        
        # Avatar et initiale
        user = request.user
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
            
        # Broadcast via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{conversation_id}',
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender_id': user.id,
                    'sender_name': user.get_full_name() or user.email,
                    'sender_avatar': avatar,
                    'sender_initial': initial,
                    'content': message.content,
                    'attachment_url': attachment.file.url,
                    'attachment_type': attachment.file_type,
                    'attachment_description': attachment.description,
                    'timestamp': message.timestamp.strftime('%H:%M'),
                }
            }
        )
        
        return JsonResponse({
            'status': 'success',
            'message_id': message.id,
            'attachment_id': attachment.id,
            'file_url': attachment.file.url,
            'attachment_type': attachment.file_type,
            'description': attachment.description
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def get_unread_count(request):
    unread_count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    
    return JsonResponse({'unread_count': unread_count})

@login_required
@require_GET
def messages_ajax(request):
    conversation_id = request.GET.get('conversation_id')
    after_id = request.GET.get('after_id')
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.client and request.user != conversation.fournisseur.user:
        raise PermissionDenied
    messages_qs = Message.objects.filter(conversation=conversation)
    if after_id:
        messages_qs = messages_qs.filter(id__gt=after_id)
    messages_qs = messages_qs.order_by('timestamp')
    messages = []
    for msg in messages_qs:
        messages.append({
            'id': msg.id,
            'sender_id': msg.sender.id,
            'sender_avatar': getattr(msg.sender, 'image', None).url if hasattr(msg.sender, 'image') and msg.sender.image else '',
            'sender_initial': msg.sender.first_name[:1].upper() if hasattr(msg.sender, 'first_name') else '',
            'content': msg.content,
            'attachment_url': msg.attachment.file.url if msg.attachment else '',
            'attachment_type': msg.attachment.file_type if msg.attachment else '',
            'time': msg.timestamp.strftime('%H:%M'),
        })
    return JsonResponse({'messages': messages})

@login_required
@require_http_methods(["POST", "GET"])
def unread_ajax(request):
    conversation_id = request.GET.get('conversation_id') or request.POST.get('conversation_id')
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user != conversation.client and request.user != conversation.fournisseur.user:
        raise PermissionDenied
    if request.method == 'POST':
        Message.objects.filter(conversation=conversation, is_read=False).exclude(sender=request.user).update(is_read=True)
        return JsonResponse({'status': 'ok'})
    else:
        count = Message.objects.filter(conversation=conversation, is_read=False).exclude(sender=request.user).count()
        return JsonResponse({'unread_count': count})

@login_required
@require_POST
def delete_conversation(request):
    conversation_id = request.POST.get('conversation_id')
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user == conversation.client or request.user == conversation.fournisseur.user:
        conversation.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=403)

@login_required
@require_POST
def delete_message(request):
    message_id = request.POST.get('message_id')
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.sender:
        message.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=403)

@login_required
@require_GET
def unread_count_per_conversation(request):
    # Retourne le nombre de messages non lus pour chaque conversation de l'utilisateur
    user = request.user
    if hasattr(user, 'is_fournisseur') and user.is_fournisseur:
        conversations = Conversation.objects.filter(fournisseur__user=user)
    else:
        conversations = Conversation.objects.filter(client=user)
    data = {}
    for conv in conversations:
        count = Message.objects.filter(conversation=conv, is_read=False).exclude(sender=user).count()
        data[conv.id] = count
    return JsonResponse({'unread_counts': data})

@login_required
@require_POST
def edit_message(request):
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        new_content = data.get('content', '').strip()
        message = Message.objects.get(id=message_id)
        if request.user != message.sender:
            return JsonResponse({'status': 'error', 'message': 'Permission refusée'}, status=403)
        message.content = new_content
        message.save(update_fields=['content'])
        return JsonResponse({'status': 'success'})
    except Message.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@require_GET
def conversations_api(request):
    user = request.user
    if hasattr(user, 'is_fournisseur') and user.is_fournisseur:
        conversations = Conversation.objects.filter(fournisseur__user=user)
    else:
        conversations = Conversation.objects.filter(client=user)
    data = []
    for conv in conversations:
        # Messages non lus reçus (jamais ceux envoyés)
        unread_qs = conv.messages.filter(is_read=False).exclude(sender=user).order_by('-timestamp')
        last_unread = unread_qs.first()
        unread_count = unread_qs.count()
        # Dernier message reçu (pour la date si tout est lu)
        last_received = conv.messages.exclude(sender=user).order_by('-timestamp').first()
        # Nom et avatar
        if hasattr(user, 'is_fournisseur') and user.is_fournisseur:
            name = conv.client.get_full_name() or conv.client.email
            avatar = conv.client.image.url if hasattr(conv.client, 'image') and conv.client.image else ''
        else:
            name = conv.fournisseur.nom
            avatar = conv.fournisseur.logo.url if conv.fournisseur.logo else ''
        data.append({
            'id': conv.id,
            'name': name,
            'avatar': avatar,
            'unread_count': unread_count,
            'last_unread_time': last_unread.timestamp.isoformat() if last_unread else None,
            'last_message_time': last_received.timestamp.isoformat() if last_received else None,
            'last_message': last_received.content if last_received else '',
            'client_id': conv.client.id,
            'fournisseur_id': conv.fournisseur.id,
        })
    return JsonResponse({'conversations': data})

@login_required
@require_GET
def user_status_api(request, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    return JsonResponse({
        'is_online': user.is_online,
        'last_seen': user.last_seen.isoformat() if user.last_seen else None,
    })
