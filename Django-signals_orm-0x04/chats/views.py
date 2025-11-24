from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message

@login_required
@cache_page(60)  # cache for 60 seconds
def message_list(request):
    # show messages for the logged-in user, optimized
    messages = Message.objects.filter(receiver=request.user).select_related('sender', 'parent_message').prefetch_related('replies')[:50]
    return render(request, 'messages.html', {'messages': messages})
