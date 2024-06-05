from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home-view'),
    path('<str:room_name>/', views.room_view, name='room-view')
]
