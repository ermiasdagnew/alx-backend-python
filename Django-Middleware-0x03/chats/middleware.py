from datetime import datetime
import logging
import time
from django.http import HttpResponseForbidden
from collections import defaultdict

# -----------------------------------------
# REQUEST LOGGING MIDDLEWARE
# -----------------------------------------
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
        return self.get_response(request)

# -----------------------------------------
# TIME-BASED ACCESS MIDDLEWARE
# -----------------------------------------
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().hour
        if now < 6 or now >= 21:
            return HttpResponseForbidden("Access to chat is restricted at this time.")
        return self.get_response(request)

# -----------------------------------------
# RATE LIMITING MIDDLEWARE
# -----------------------------------------
class OffensiveLanguageMiddleware:
    message_logs = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60
            limit = 5

            self.message_logs[ip] = [t for t in self.message_logs[ip] if now - t < window]

            if len(self.message_logs[ip]) >= limit:
                return HttpResponseForbidden("Message limit exceeded. Please wait a minute.")

            self.message_logs[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x = request.META.get('HTTP_X_FORWARDED_FOR')
        return x.split(',')[0].strip() if x else request.META.get('REMOTE_ADDR')

# -----------------------------------------
# ROLE PERMISSION MIDDLEWARE
# -----------------------------------------
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if not user or getattr(user, 'role', None) not in ['admin', 'moderator']:
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)
