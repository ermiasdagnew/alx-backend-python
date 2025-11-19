from django.http import HttpResponseForbidden
import logging
from datetime import datetime, timedelta
from django.utils.timezone import now

# Task 1: Logging User Requests
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(filename='requests.log', format='%(message)s', level=logging.INFO)

    def __call__(self, request):
        user = request.user if getattr(request, 'user', None) and request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)

# Task 2: Restrict Access by Time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = now().hour
        if current_hour >= 21 or current_hour < 6:
            return HttpResponseForbidden("Access to chat is restricted at this time.")
        return self.get_response(request)

# Task 3: Offensive Language / Rate Limiting
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}
        self.MAX_REQUESTS = 5
        self.WINDOW_MINUTES = 1

    def __call__(self, request):
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR", "unknown")
            now_time = now()
            if ip not in self.requests:
                self.requests[ip] = []
            self.requests[ip] = [t for t in self.requests[ip] if now_time - t < timedelta(minutes=self.WINDOW_MINUTES)]
            if len(self.requests[ip]) >= self.MAX_REQUESTS:
                return HttpResponseForbidden("Message limit exceeded.")
            self.requests[ip].append(now_time)
        return self.get_response(request)

# Task 4: Role Permission Middleware
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if not (user and user.is_authenticated and (user.is_staff or user.is_superuser)):
            return HttpResponseForbidden("Insufficient permissions.")
        return self.get_response(request)
