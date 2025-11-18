# apps/chats/middleware.py
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

# ---------------------------
# Task 1: Request Logging
# ---------------------------
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = 'apps/chats/requests.log'

    def __call__(self, request):
        user = getattr(request, 'user', None)
        user_info = user.username if user and user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user_info} - Path: {request.path}\n"

        # Write log to file
        with open(self.log_file, 'a') as f:
            f.write(log_message)

        response = self.get_response(request)
        return response


# ---------------------------
# Task 2: Restrict Chat Access by Time
# ---------------------------
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 6 AM (6) and 9 PM (21)
        if 6 <= current_hour < 21:
            return self.get_response(request)
        else:
            return HttpResponseForbidden("Chat access is restricted between 9PM and 6AM.")


# ---------------------------
# Task 3: Offensive Language / Rate Limiting
# ---------------------------
class OffensiveLanguageMiddleware:
    # Limit: 5 messages per minute per IP
    RATE_LIMIT = 5
    TIME_WINDOW = timedelta(minutes=1)
    ip_message_records = {}  # { ip: [(timestamp1), (timestamp2), ...] }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        if request.method == "POST":  # count only POST messages
            now = datetime.now()
            records = self.ip_message_records.get(ip, [])

            # Remove old timestamps
            records = [ts for ts in records if now - ts < self.TIME_WINDOW]

            if len(records) >= self.RATE_LIMIT:
                return HttpResponseForbidden("Message rate limit exceeded. Try again later.")

            records.append(now)
            self.ip_message_records[ip] = records

        return self.get_response(request)

    def get_client_ip(self, request):
        # Get real IP even if behind proxy
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# ---------------------------
# Task 4: Role Permission
# ---------------------------
class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            if user.is_superuser or getattr(user, 'role', None) in ['admin', 'moderator']:
                return self.get_response(request)
            else:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        else:
            return HttpResponseForbidden("You must be logged in to access this resource.")
