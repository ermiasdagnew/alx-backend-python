# chats/middleware.py

from datetime import datetime
from time import time
from django.http import HttpResponseForbidden


# 1. Log user requests
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request.user, 'username', 'Anonymous')
        log_line = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open('requests.log', 'a') as f:
            f.write(log_line)
        response = self.get_response(request)
        return response


# 2. Restrict chat access by time (outside 6AM–9PM)
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().hour
        if now >= 21 or now < 6:
            return HttpResponseForbidden("Chat access is not allowed at this time.")
        return self.get_response(request)


# 3. Limit number of chat messages per IP (rate limiting)
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_tracker = {}  # {ip: [timestamp1, timestamp2, ...]}

    def __call__(self, request):
        if request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR', '')
            now = time()
            self.ip_tracker.setdefault(ip, [])
            # Keep only timestamps in the last 60 seconds
            self.ip_tracker[ip] = [t for t in self.ip_tracker[ip] if now - t < 60]
            if len(self.ip_tracker[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded. Try again later.")
            self.ip_tracker[ip].append(now)
        return self.get_response(request)


# 4. Enforce user role permissions
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(request.user, 'is_authenticated', False):
            return HttpResponseForbidden("Authentication required.")
        if not getattr(request.user, 'role', None) in ['admin', 'moderator']:
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)
