from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='pass')
        self.receiver = User.objects.create_user(username='bob', password='pass')

    def test_notification_created_on_message_save(self):
        Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello')
        self.assertEqual(Notification.objects.count(), 1)
