from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation, IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation, IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.validated_data['conversation']
        if request.user not in conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
