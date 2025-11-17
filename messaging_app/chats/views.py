from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    # Override list() to ensure paginated response contains page.paginator.count
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # <-- contains page.paginator.count
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
