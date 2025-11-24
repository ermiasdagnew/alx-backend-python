from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from messaging.models import Message

User = get_user_model()

# -----------------------------
# Existing message list view
# -----------------------------
@login_required
@cache_page(60)  # cache for 60 seconds
def message_list(request):
    messages = Message.objects.filter(
        receiver=request.user
    ).select_related('sender', 'parent_message').prefetch_related('replies')[:50]
    return render(request, 'messages.html', {'messages': messages})

# -----------------------------
# New delete_user view
# -----------------------------
@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        return redirect('home')  # redirect after deletion
    return HttpResponseForbidden("You can only delete your account via POST request")
