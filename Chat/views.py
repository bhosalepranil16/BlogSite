from django.contrib.auth.models import User
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect


# Create your views here.

def chat_page(request, room_name):
    users = room_name.split('_')
    if len(users) != 2:
        return HttpResponseRedirect(reverse('index_page'))

    if users[0] == users[1]:
        return HttpResponseRedirect(reverse('index_page'))

    try:
        user0 = User.objects.get(username=users[0])
        user1 = User.objects.get(username=users[1])
    except:
        return HttpResponseRedirect(reverse('index_page'))

    if request.user.username != user0.username and request.user.username != user1.username:
        return HttpResponseRedirect(reverse('index_page'))

    if user0.username < user1.username:
        room_name = user0.username + '_' + user1.username
    else:
        room_name = user1.username + '_' + user0.username

    return render(request, 'Chat/index.html', context={
        'room_name': room_name
    })
