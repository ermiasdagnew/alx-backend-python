MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.chats.middleware.RequestLoggingMiddleware',
    'apps.chats.middleware.RestrictAccessByTimeMiddleware',
    'apps.chats.middleware.OffensiveLanguageMiddleware',
    'apps.chats.middleware.RolePermissionMiddleware',
]