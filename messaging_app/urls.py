from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('messaging_app.chats.auth')),  # JWT auth endpoints
    path('api/chats/', include('messaging_app.chats.urls')),  # chat endpoints
]
