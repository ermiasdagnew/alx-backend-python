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
