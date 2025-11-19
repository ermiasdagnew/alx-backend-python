import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            'sender': ['exact'],
            'created_at': ['gte', 'lte'],
        }
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import MessagePagination

class MessageListView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
