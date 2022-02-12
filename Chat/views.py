from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from .models import MessageModel


# Create your views here.

def chat_page(request, room_name):
    users = room_name.split('_')
    if len(users) != 2:
        return HttpResponseRedirect(reverse('index_page'))

    if users[0] == users[1]:
        return HttpResponseRedirect(reverse('index_page'))

    try:
        sender = User.objects.get(username=users[0])
        receiver = User.objects.get(username=users[1])
    except:
        return HttpResponseRedirect(reverse('index_page'))

    if sender.username != request.user.username:
        return HttpResponseRedirect(reverse('index_page'))

    if sender.username < receiver.username:
        room_name = sender.username + '_' + receiver.username
    else:
        room_name = receiver.username + '_' + sender.username

        # messages = MessageModel.objects.filter(room_name=room_name).order_by('-created_at')

    return render(request, 'Chat/index.html', context={
        'messages': MessageModel.objects.filter(room_name=room_name).order_by('created_at'),
        'room_name': room_name,
        'sender_username': sender.username,
        'sender_id': sender.id,
        'receiver_username': receiver.username,
        'receiver_id': receiver.id,
    })
