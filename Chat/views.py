from django.shortcuts import render


# Create your views here.

def chat_page(request, room_name):
    return render(request, 'Chat/index.html')
