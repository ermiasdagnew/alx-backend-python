from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') else 'Anonymous'
        log_line = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open('apps/chats/requests.log', 'a') as f:
            f.write(log_line)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now_hour = datetime.now().hour
        if not (6 <= now_hour <= 21):
            return HttpResponseForbidden('Chat is only available between 6AM and 9PM.')
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    ip_counts = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            now = datetime.now()
            self.ip_counts[ip] = [t for t in self.ip_counts[ip] if now - t < timedelta(minutes=1)]
            if len(self.ip_counts[ip]) >= 5:
                return HttpResponseForbidden('Message limit exceeded. Try again later.')
            self.ip_counts[ip].append(now)
        return self.get_response(request)

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            user = getattr(request, 'user', None)
            if not user or not user.is_authenticated:
                return HttpResponseForbidden('You must be logged in.')
            if not (user.is_staff or getattr(user, 'role', '').lower() in ['admin', 'moderator']):
                return HttpResponseForbidden('Insufficient permissions.')
        return self.get_response(request)