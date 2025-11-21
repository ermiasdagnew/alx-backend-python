MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # YOUR CUSTOM MIDDLEWARE (Tasks 1–4)
    'chats.middleware.RequestLoggingMiddleware',      # Task 1
    'chats.middleware.RestrictAccessByTimeMiddleware',# Task 2
    'chats.middleware.OffensiveLanguageMiddleware',   # Task 3
    'chats.middleware.RolePermissionMiddleware',      # Task 4

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
