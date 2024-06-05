from chat.models import Room, Message
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import QuerySet


class TestRoom(TestCase):
    '''
    Test room
    '''

    def setUp(self) -> None:
        self.room = Room.objects.create(name="testing")

    def test_name(self) -> None:
        '''
        Test the name of room
        '''
        online_users = self.room.online_users
        self.assertEqual(self.room.name, 'testing')

    def test_number_of_members(self) -> None:
        '''
        test the number of online user count
        '''
        self.assertEqual(self.room.get_online_user_count(), 0)
        user = User.objects.create(username='bion', password=1234)
        self.room.join_room(user)
        self.assertEqual(self.room.get_online_user_count(), 1)

    def test_leave_room(self) -> None:
        '''
        test leaving a room
        '''
        user = User.objects.create(username='bion', password=1234)
        self.room.join_room(user)
        self.assertEqual(self.room.get_online_user_count(), 1)

        self.room.leave_room(user)
        self.assertEqual(self.room.get_online_user_count(), 0)

    def test__str__(self) -> None:
        '''
        testing the __str__ method
        '''
        self.assertEqual(str(self.room), 'Name: testing Total user: 0')


class TestMessages(TestCase):
    '''
    Test that the messages passed
    '''

    def setUp(self) -> None:
        '''
        set up a message object for every test
        '''
        self.user = User.objects.create(username='bion', password=1234)
        self.room = Room.objects.create(name="testing")
        self.message = Message.objects.create(
            user=self.user,
            room=self.room,
            content='testing'
        )

    def test_user(self) -> None:
        '''
        test the user and the foreign key
        '''
        self.assertEqual(self.message.user, self.user)
        self.assertIsInstance(self.user.message_set.all(), QuerySet)
        self.assertIsInstance(self.user.message_set.all()[0], Message)

    def test_room(self) -> None:
        '''
        test the room is a foreign key
        '''
        self.assertEqual(self.message.room, self.room)
        self.assertIsInstance(self.room.message_set.all(), QuerySet)
        self.assertIsInstance(self.room.message_set.all()[0], Message)

    def test_content(self) -> None:
        '''
        test the content
        '''
        self.assertEqual(self.message.content, 'testing')
