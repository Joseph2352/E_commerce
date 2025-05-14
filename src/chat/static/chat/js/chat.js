// chat.js - gestion du chat temps réel et de l'UI

// Les variables suivantes sont injectées par le template :
// conversationId, userId, otherUserId, userName

const sendBtn = document.getElementById('send-btn');
const messageInput = document.getElementById('message-input');

const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
let chatSocket = null;
let canSend = false;
let selectedImageFile = null;

// Détection du rôle utilisateur pour la génération d'URL
window.isFournisseur = typeof isFournisseur !== 'undefined' ? isFournisseur : (
    typeof USER_IS_FOURNISSEUR !== 'undefined' ? USER_IS_FOURNISSEUR : false
);

// Ouvre le WebSocket uniquement si la conversation existe
if (conversationId && conversationId !== '' && conversationId !== 'null') {
    chatSocket = new WebSocket(
        wsScheme + '://' + window.location.host + '/ws/chat/' + conversationId + '/'
    );
    canSend = true;
}

function setSendBtnState() {
    if (!sendBtn || !messageInput) return;
    sendBtn.disabled = !(messageInput.value.trim() || selectedImageFile);
}

if (messageInput) {
messageInput.addEventListener('input', setSendBtnState);
setSendBtnState();
}
if (sendBtn) {
    sendBtn.onclick = sendMessageWS;
}

// Aperçu d'image dans la zone d'input (ChatGPT style)
const imagePreviewContainer = document.getElementById('image-preview-container');
const previewImage = document.getElementById('preview-image');
const removeImageBtn = document.getElementById('remove-image-btn');

const fileInput = document.getElementById('file-input');
if (fileInput) {
    fileInput.addEventListener('change', function() {
        const file = fileInput.files[0];
        if (!file) return;
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                if (previewImage && imagePreviewContainer) {
                    previewImage.src = e.target.result;
                    imagePreviewContainer.style.display = 'flex';
                }
                selectedImageFile = file;
                setSendBtnState();
            };
            reader.readAsDataURL(file);
        } else {
            uploadFile(file, messageInput ? messageInput.value.trim() : '');
            fileInput.value = '';
        }
    });
}
if (removeImageBtn) {
    removeImageBtn.addEventListener('click', function() {
        if (previewImage && imagePreviewContainer) {
            previewImage.src = '#';
            imagePreviewContainer.style.display = 'none';
        }
        if (fileInput) fileInput.value = '';
        selectedImageFile = null;
        setSendBtnState();
    });
}

// Surcharge l'envoi de message pour gérer l'image + texte
function sendMessageWS() {
    const content = messageInput && messageInput.value ? messageInput.value.trim() : '';
    // Si une image est sélectionnée, on l'envoie avec le texte comme description
    if (selectedImageFile) {
        uploadFile(selectedImageFile, content);
        // Reset UI
        if (previewImage) previewImage.src = '#';
        if (imagePreviewContainer) imagePreviewContainer.style.display = 'none';
        if (fileInput) fileInput.value = '';
        selectedImageFile = null;
        if (messageInput) messageInput.value = '';
        setSendBtnState();
        // NE PAS envoyer le texte via WebSocket
        return;
    }
    // Sinon, message texte classique
    if (!content) return;
    if (canSend && chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        chatSocket.send(JSON.stringify({
            'type': 'chat_message',
            'sender_id': userId,
            'content': content,
            'other_user_id': otherUserId
        }));
        if (messageInput) messageInput.value = '';
        setSendBtnState();
    } else {
        // Fallback AJAX
        fetch('/chat/send/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                content: content,
                other_user_id: otherUserId
            })
        }).then(resp => resp.json()).then(data => {
            if (data.status === 'success') {
                if (messageInput) messageInput.value = '';
                setSendBtnState();
            } else {
                alert('Erreur lors de l\'envoi du message.');
            }
        });
    }
}

if (messageInput) {
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessageWS();
    }
});
}

// Gestion des messages reçus
function renderMessage(msg) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + (msg.sender_id == userId ? 'sent' : 'received');

    // Avatar
    let avatarHtml = '';
    if (msg.sender_avatar && msg.sender_avatar !== '') {
        avatarHtml = `<span class='message-avatar'><img src='${msg.sender_avatar}' style='width:100%;height:100%;border-radius:50%'></span>`;
    } else {
        avatarHtml = `<span class='message-avatar' style='background:${msg.sender_id == userId ? '#ff6600' : '#2563eb'}'>${msg.sender_initial || '?'}</span>`;
    }

    // Contenu
    let contentHtml = `<div class='message-content'>${msg.content || ''}`;
    if (msg.attachment_url) {
        if (msg.attachment_type && msg.attachment_type.startsWith('image')) {
            contentHtml += `
                <div class='attachments'>
                    <div class='attachment'>
                        <img src='${msg.attachment_url}' 
                             alt='Image' 
                             class='attachment-image'
                             onclick='showFullImage("${msg.attachment_url}", "${msg.attachment_description || ''}")'
                             style='cursor: pointer;'>
                        ${msg.attachment_description ? `<div class='attachment-description'>${msg.attachment_description}</div>` : ''}
                    </div>
                </div>`;
        } else {
            contentHtml += `
                <div class='attachments'>
                    <div class='attachment'>
                        <a href='${msg.attachment_url}' class='attachment-file' target='_blank'>
                            <i class='fas fa-file'></i>
                            <span>Voir le fichier</span>
                        </a>
                        ${msg.attachment_description ? `<div class='attachment-description'>${msg.attachment_description}</div>` : ''}
                    </div>
                </div>`;
        }
    }
    contentHtml += '</div>';

    messageDiv.innerHTML = avatarHtml + contentHtml + `<span class='message-time'>${msg.timestamp || msg.time || ''}</span>`;
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}

if (chatSocket) {
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'chat_message') {
            renderMessage(data.message);
            console.log('Message reçu via WebSocket:', data.message);
        }
        if (data.type === 'typing') {
            const typingDiv = document.getElementById('typing-indicator');
            if (data.user !== userName) {
                typingDiv.textContent = data.user + ' est en train d\'écrire...';
                setTimeout(() => { typingDiv.textContent = ''; }, 2000);
            }
        }
        if (data.type === 'new_conversation') {
            addConversationToSidebar(data.conversation);
        }
    };
    chatSocket.onclose = function(e) {
        canSend = false;
        if (sendBtn) sendBtn.disabled = true;
        console.error('Chat socket closed');
    };
    setInterval(() => {
        if (chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.send(JSON.stringify({type: 'ping'}));
        }
    }, 30000); // toutes les 30 secondes
} else {
    if (sendBtn) sendBtn.disabled = true;
}

// Scroll auto en bas
function scrollToBottom() {
    const messagesDiv = document.getElementById('messages');
    if (messagesDiv) messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Utilitaire pour formater la date (ex: "il y a 5 min" ou HH:mm)
function formatTime(isoString) {
    if (!isoString) return '';
    const date = new Date(isoString);
    const now = new Date();
    const diff = (now - date) / 1000; // en secondes
    if (diff < 60) return '0 minute';
    if (diff < 3600) return Math.floor(diff/60) + ' minutes';
    if (diff < 86400) return Math.floor(diff/3600) + ' heures';
    // Sinon, date locale courte
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
}

function refreshConversationList() {
    fetch('/chat/conversations_api/')
        .then(resp => resp.json())
        .then(data => {
            console.log('Conversations API:', data); // Debug
            const list = document.querySelector('.conversation-list');
            if (!list) return;
            list.innerHTML = '';
            if (!data.conversations) {
                list.innerHTML = '<div class="no-conversation"><h2>Erreur API : clé "conversations" manquante</h2></div>';
                return;
            }
            if (data.conversations.length === 0) {
                list.innerHTML = '<div class="no-conversation"><h2>Aucune conversation</h2></div>';
                return;
            }
            data.conversations.forEach(conv => {
                let url = '';
                if (window.isFournisseur === 'true') {
                    url = `/chat/room/${conv.client_id}/?conversation_id=${conv.id}`;
                } else {
                    url = `/chat/room/${conv.fournisseur_id}/?conversation_id=${conv.id}`;
                }
                let dateStr = '';
                let badgeHtml = '';
                if (conv.unread_count > 0 && conv.last_unread_time) {
                    dateStr = formatTime(conv.last_unread_time);
                    badgeHtml = `<span class="unread-badge">${conv.unread_count}</span>`;
                }
                const wrapper = document.createElement('div');
                wrapper.className = 'conversation-wrap';

                const a = document.createElement('a');
                a.href = url;
                a.className = 'conversation-item' + (conv.id == conversationId ? ' active' : '');
                a.setAttribute('data-conversation-id', conv.id);
                a.innerHTML = `
                    <div class="conversation-avatar">
                        ${conv.avatar ? `<img src="${conv.avatar}" alt="Avatar">` : `<div class="avatar-placeholder">${conv.name[0].toUpperCase()}</div>`}
                    </div>
                    <div class="conversation-info">
                        <h3>${conv.name}</h3>
                        ${dateStr ? `<span class="conversation-time">${dateStr}</span>` : ''}
                        ${badgeHtml}
                    </div>
                `;

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'delete-conversation';
                deleteBtn.setAttribute('data-id', conv.id);
                deleteBtn.setAttribute('title', 'Supprimer');
                deleteBtn.innerHTML = '&#10005;';

                wrapper.appendChild(deleteBtn);
                wrapper.appendChild(a);
                list.appendChild(wrapper);

                });
            })
            .catch(err => {
                const list = document.querySelector('.conversation-list');
                if (list) list.innerHTML = '<div class="no-conversation"><h2>Erreur lors du chargement des conversations</h2></div>';
                console.error('Erreur API:', err);
            });
}

// Marquer les messages comme lus et mettre à jour le badge + la liste
function markAsRead(conversationId) {
    fetch(`/chat/unread/?conversation_id=${conversationId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    }).then(() => {
        refreshConversationList();
    });
}

// Scroll auto au chargement et après chaque nouveau message
window.addEventListener('DOMContentLoaded', scrollToBottom);
const observer = new MutationObserver(scrollToBottom);
const messagesDiv = document.getElementById('messages');
if (messagesDiv) observer.observe(messagesDiv, { childList: true });

// Fonction pour obtenir le token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Gestion de l'emoji picker (liste d'emojis native)

// Gestion de l'envoi de pièce jointe (image ou fichier)
const attachmentBtn = document.getElementById('attachment-btn');
if (attachmentBtn && fileInput) {
    attachmentBtn.addEventListener('click', function() {
        fileInput.click();
    });
}

// Fonction pour afficher la prévisualisation de l'image
function showImagePreviewModal(imageUrl, file) {
    const modal = document.createElement('div');
    modal.className = 'image-preview-modal';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0,0,0,0.8)';
    modal.style.zIndex = '1000';
    modal.style.display = 'flex';
    modal.style.flexDirection = 'column';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    
    const previewContainer = document.createElement('div');
    previewContainer.style.maxWidth = '80%';
    previewContainer.style.maxHeight = '80%';
    previewContainer.style.backgroundColor = 'white';
    previewContainer.style.padding = '20px';
    previewContainer.style.borderRadius = '8px';
    
    const img = document.createElement('img');
    img.src = imageUrl;
    img.style.maxWidth = '100%';
    img.style.maxHeight = '60vh';
    img.style.objectFit = 'contain';
    
    const descriptionInput = document.createElement('textarea');
    descriptionInput.placeholder = 'Ajouter une description (optionnel)';
    descriptionInput.style.width = '100%';
    descriptionInput.style.marginTop = '10px';
    descriptionInput.style.padding = '8px';
    descriptionInput.style.border = '1px solid #ddd';
    descriptionInput.style.borderRadius = '4px';
    
    const buttonContainer = document.createElement('div');
    buttonContainer.style.marginTop = '10px';
    buttonContainer.style.display = 'flex';
    buttonContainer.style.gap = '10px';
    
    const sendButton = document.createElement('button');
    sendButton.textContent = 'Envoyer';
    sendButton.className = 'btn btn-primary';
    sendButton.onclick = () => {
        uploadFile(file, descriptionInput.value);
        modal.remove();
    };
    
    const cancelButton = document.createElement('button');
    cancelButton.textContent = 'Annuler';
    cancelButton.className = 'btn btn-secondary';
    cancelButton.onclick = () => {
        modal.remove();
        fileInput.value = '';
    };
    
    buttonContainer.appendChild(sendButton);
    buttonContainer.appendChild(cancelButton);
    
    previewContainer.appendChild(img);
    previewContainer.appendChild(descriptionInput);
    previewContainer.appendChild(buttonContainer);
    modal.appendChild(previewContainer);
    
    document.body.appendChild(modal);
}

// Fonction pour uploader le fichier
function uploadFile(file, description = '') {
    const formData = new FormData();
    formData.append('conversation_id', conversationId);
    formData.append('file', file);
    formData.append('description', description);
    
    fetch('/chat/upload/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    }).then(resp => resp.json()).then(data => {
        if (data.status === 'success') {
            messageInput.value = '';
            setSendBtnState();
        } else {
            alert('Erreur lors de l\'upload de la pièce jointe.');
        }
    });
}

// Fonction pour afficher l'image en plein écran
function showFullImage(imageUrl, description = '') {
    const modal = document.createElement('div');
    modal.className = 'full-image-modal';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0,0,0,0.9)';
    modal.style.zIndex = '1000';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.cursor = 'zoom-out';
    
    const img = document.createElement('img');
    img.src = imageUrl;
    img.style.maxWidth = '90%';
    img.style.maxHeight = '90%';
    img.style.objectFit = 'contain';
    
    if (description) {
        const descDiv = document.createElement('div');
        descDiv.className = 'image-description';
        descDiv.style.position = 'absolute';
        descDiv.style.bottom = '20px';
        descDiv.style.left = '50%';
        descDiv.style.transform = 'translateX(-50%)';
        descDiv.style.color = 'white';
        descDiv.style.padding = '10px 20px';
        descDiv.style.backgroundColor = 'rgba(0,0,0,0.7)';
        descDiv.style.borderRadius = '4px';
        descDiv.textContent = description;
        modal.appendChild(descDiv);
    }
    
    modal.appendChild(img);
    document.body.appendChild(modal);
    
    // Fermer la modal au clic
    modal.addEventListener('click', () => {
        modal.remove();
    });
}

function addConversationToSidebar(conversation) {
    const list = document.querySelector('.conversation-list');
    if (!list) return;
    // Vérifie si la conversation existe déjà
    if (list.querySelector(`[data-conversation-id='${conversation.id}']`)) return;
    const a = document.createElement('a');
    a.href = `/chat/room/${conversation.id}/?conversation_id=${conversation.id}`;
    a.className = 'conversation-item active';
    a.setAttribute('data-conversation-id', conversation.id);
    a.innerHTML = `
        <div class="conversation-avatar">
            ${conversation.client_avatar ? `<img src="${conversation.client_avatar}" alt="Avatar">` : `<div class="avatar-placeholder">${conversation.client_name[0].toUpperCase()}</div>`}
        </div>
        <div class="conversation-info">
            <h3>${conversation.client_name}</h3>
            <span class="conversation-time">${conversation.last_message_time || ''}</span>
        </div>
    `;
    list.prepend(a);
}

// Suppression conversation
document.querySelectorAll('.delete-conversation').forEach(btn => {
    btn.onclick = function(e) {
        e.stopPropagation();
        if (confirm('Supprimer cette conversation ?')) {
            fetch('/chat/delete_conversation/', {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                body: new URLSearchParams({conversation_id: btn.dataset.id})
            }).then(resp => resp.json()).then(data => {
                if (data.status === 'success') {
                    btn.closest('.conversation-item').remove();
                }
            });
        }
    }
});

// Suppression message
document.querySelectorAll('.delete-message').forEach(btn => {
    btn.onclick = function(e) {
        e.stopPropagation();
        if (confirm('Supprimer ce message ?')) {
            fetch('/chat/delete_message/', {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                body: new URLSearchParams({message_id: btn.dataset.id})
            }).then(resp => resp.json()).then(data => {
                if (data.status === 'success') {
                    btn.closest('.message').remove();
                }
            });
        }
    }
});

// Chargement dynamique des badges non lus
function updateUnreadBadges() {
    fetch('/chat/unread_count_per_conversation/')
        .then(resp => resp.json())
        .then(data => {
            if (data.unread_counts) {
                document.querySelectorAll('.conversation-item').forEach(item => {
                    const convId = item.getAttribute('data-conversation-id');
                    const badge = item.querySelector('.unread-badge');
                    const count = data.unread_counts[convId] || 0;
                    if (badge) {
                        badge.textContent = count;
                        badge.style.display = count > 0 ? 'inline' : 'none';
                    }
                });
            }
        });
}

// Appelle ces fonctions au chargement
window.addEventListener('DOMContentLoaded', function() {
    refreshConversationList();
    bindDeleteConversation();
    bindDeleteMessage();
    updateUnreadBadges();
});

// Gestion édition/suppression inline des messages (délégation sur #messages)
if (messagesDiv) {
    messagesDiv.addEventListener('click', function(e) {
        // Actions seulement sur les messages envoyés par l'utilisateur
        const msgDiv = e.target.closest('.message.sent');
        if (!msgDiv) return;
        // Afficher actions au clic sur le message (mobile)
        if (!e.target.closest('.message-actions')) {
            document.querySelectorAll('.message.selected').forEach(m => m.classList.remove('selected'));
            msgDiv.classList.add('selected');
        }
        // Édition message
        if (e.target.closest('.edit-message')) {
            const contentDiv = msgDiv.querySelector('.message-content');
            const oldText = contentDiv.innerText;
            contentDiv.innerHTML = `<input type="text" class="edit-input" value="${oldText}"> <button class="save-edit">OK</button>`;
            contentDiv.querySelector('.edit-input').focus();
        }
        // Sauvegarde édition
        if (e.target.classList.contains('save-edit')) {
            const input = msgDiv.querySelector('.edit-input');
            const newText = input.value;
            const messageId = msgDiv.dataset.messageId;
            fetch('/chat/edit_message/', {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json'},
                body: JSON.stringify({message_id: messageId, content: newText})
            }).then(resp => resp.json()).then(data => {
                if (data.status === 'success') {
                    msgDiv.querySelector('.message-content').textContent = newText;
                } else {
                    alert('Erreur lors de la modification.');
                }
            });
        }
        // Suppression message
        if (e.target.closest('.delete-message')) {
            if (confirm('Supprimer ce message ?')) {
                const btn = e.target.closest('.delete-message');
                const messageId = btn.dataset.id;
                fetch('/chat/delete_message/', {
                    method: 'POST',
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    body: new URLSearchParams({message_id: messageId})
                }).then(resp => resp.json()).then(data => {
                    if (data.status === 'success') {
                        msgDiv.remove();
                    }
                });
            }
        }
    });
}