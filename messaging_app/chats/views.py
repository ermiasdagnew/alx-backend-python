from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from .models import Chat, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations (chats)
    """
    queryset = Chat.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def create(self, request, *args, **kwargs):
        """
        Override create to allow creating a new conversation with participants
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()
        return Response(self.get_serializer(chat).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']
    ordering = ['timestamp']

    def create(self, request, *args, **kwargs):
        """
        Override create to send a message to an existing conversation
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(self.get_serializer(message).data, status=status.HTTP_201_CREATED)
