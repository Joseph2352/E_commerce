from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from django.utils.timezone import now



from .models import *
# Create your views here.

def home(request):
    return render(request, 'chat/home.html')

def room(request , room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request , 'chat/room.html' , {
        'username' : username ,
        'room' : room ,
        'room_details' : room_details,
        'static_version': now().timestamp()
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name = room).exists():
        return redirect( room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name = room)
        new_room.save()
        return redirect( room + '/?username=' + username)
    
def send(request):
    message = request.POST.get('message')
    username = request.POST.get('username')
    room_id = request.POST.get('room_id')
    print(f"{message} {username} {room_id}")
    new_message = Message.objects.create(value= message , user = username , room = room_id)
    new_message.save()
    return HttpResponse('Message envoyé avec succès')

def getMessages(request , room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room = room_details.id).order_by('date')
    return JsonResponse({"messages" :list(messages.values())})