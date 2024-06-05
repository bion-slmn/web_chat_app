from .models import Room
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home_view(request: HttpRequest) -> HttpResponse:
    '''
    display the home page
    '''
    content = {'rooms': Room.objects.all()}
    return render(request, 'chat/index.html', content)


def room_view(request: HttpRequest, room_name: str) -> HttpResponse:
    '''
    display the content of a room
    '''
    chat_room, created = Room.objects.get_or_create(name=room_name)
    content = {'room': chat_room}
    return render(request, 'chat/room.html', content)
