# chats/middleware.py
from datetime import datetime
import logging

# Configure a logger to write to a file
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', 'Anonymous')
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().hour
        # Restrict access outside 6AM - 9PM
        if now < 6 or now >= 21:
            return HttpResponseForbidden("Access to chat is restricted at this time.")
        response = self.get_response(request)
        return response
# chats/middleware.py
import time
from django.http import HttpResponseForbidden
from collections import defaultdict

class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of chat messages a user can send
    within a time window (e.g., 5 messages per minute) based on their IP address.
    """

    # Class-level dictionary to track messages per IP
    message_logs = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":  # Only count POST requests (messages)
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 1 minute
            limit = 5    # max messages per minute

            # Clean up old timestamps outside the time window
            self.message_logs[ip] = [t for t in self.message_logs[ip] if now - t < window]

            if len(self.message_logs[ip]) >= limit:
                return HttpResponseForbidden("Message limit exceeded. Please wait a minute.")

            # Log current message timestamp
            self.message_logs[ip].append(now)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
# chats/middleware.py
from django.http import HttpResponseForbidden

class RolepermissionMiddleware:
    """
    Middleware to restrict access to certain actions based on user role.
    Only 'admin' and 'moderator' users are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

        # If user is not authenticated or role is not allowed, return 403
        if not user or not getattr(user, 'role', None) in ['admin', 'moderator']:
            return HttpResponseForbidden("You do not have permission to access this resource.")

        response = self.get_response(request)
        return response
