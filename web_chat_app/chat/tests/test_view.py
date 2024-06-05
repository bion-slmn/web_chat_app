from chat.views import home_view, room_view
from chat.models import Room
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest, HttpResponse


class TestHomeView(TestCase):
    '''
    test the home view
    '''

    def setUp(self) -> None:
        '''
        set up to run at the begining of every test
        '''
        self.rooms = [Room(name="Living Room"), Room(name="Kitchen")]
        Room.objects.bulk_create(self.rooms)
        self.client = Client()  # Initialize the client
        self.response = self.client.get(reverse('home-view'))

    def test_response(self) -> None:
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response, HttpResponse)

    def test_context(self) -> None:
        self.assertContains(self.response, "Living Room")
        self.assertContains(self.response, "Kitchen")
        self.assertIn('rooms', self.response.context)

    def test_template_used(self) -> None:
        self.assertTemplateUsed(self.response, 'chat/index.html')


class TestRoomView(TestCase):
    def setUp(self) -> None:
        '''
        set up to run at the begining of every test
        '''
        self.client = Client()  # Initialize the client
        self.response = self.client.get(reverse('room-view', args=['testing']))

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(self.response, HttpResponse)

    def test_room_creation(self) -> None:
        self.assertEqual(Room.objects.count(), 1)
        self.assertTrue(Room.objects.filter(name='testing').exists())

    def test_template_used(self) -> None:
        self.assertTemplateUsed(self.response, 'chat/room.html')

    def test_context_data(self) -> None:
        self.assertIn('rooms', self.response.context)
        self.assertEqual(self.response.context['rooms'].name, 'testing')
