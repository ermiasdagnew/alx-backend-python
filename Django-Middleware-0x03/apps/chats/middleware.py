# apps/chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', 'Anonymous')
        log_line = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open('apps/chats/requests.log', 'a') as f:
            f.write(log_line)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 6 AM (6) and 9 PM (21)
        if not (6 <= current_hour < 21):
            return HttpResponseForbidden("Chat access is restricted at this time.")
        response = self.get_response(request)
        return response
