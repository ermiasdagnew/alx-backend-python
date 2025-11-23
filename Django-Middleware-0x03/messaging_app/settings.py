MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    ...
    'chats.middleware.RequestLoggingMiddleware',
]
MIDDLEWARE.append('chats.middleware.OffensiveLanguageMiddleware')
