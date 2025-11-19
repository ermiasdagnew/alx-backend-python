from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'total_messages': self.page.paginator.count,
            'messages': data
        })
