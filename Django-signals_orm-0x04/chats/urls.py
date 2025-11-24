from django.urls import path
from .views import message_list, delete_user

urlpatterns = [
    path('', message_list, name='message_list'),
    path('delete/', delete_user, name='delete_user'),
]
