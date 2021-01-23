from django.urls import path

from .views import *

urlpatterns = [
    path('<slug:user_id>/', room, name='room'),
]