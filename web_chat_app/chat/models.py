from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    '''
    a chat room where more than one user can communicate
    '''
    name = models.CharField(max_length=50)
    online_users = models.ManyToManyField(to=User, blank=True)

    def get_online_user_count(self) -> int:
        '''
        get the number of user in a room
        '''
        return self.online_users.count()

    def join_room(self, user: User) -> None:
        '''
        add a user to the room
        '''
        self.online_users.add(user)
        self.save()

    def leave_room(self, user: User) -> None:
        '''
        remove a user from a room
        '''
        self.online_users.remove(user)
        self.save()

    def __str__(self) -> str:
        '''
        a description of a room
        '''
        return f'Name: {self.name} Total user: {self.get_online_user_count()}'


class Message(models.Model):
    '''
    this is the message of the user
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> None:
        '''
        the description of the message
        '''
        return f'{self.user.username}: {self.content} [{self.created_at}]'
