from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages as django_messages
from messaging.models import Message, MessageHistory

# -----------------------------------------
# List messages for logged-in user (received messages)
# -----------------------------------------
@login_required
@cache_page(60)
def message_list(request):
    messages_qs = Message.objects.filter(
        receiver=request.user
    ).select_related('sender', 'parent_message').prefetch_related('replies')[:50]

    return render(request, 'messages.html', {'messages': messages_qs})


# -----------------------------------------
# Display only unread messages (Task 4)
# -----------------------------------------
@login_required
def unread_messages(request):
    """
    Display unread messages using the custom manager method unread_for_user.
    Optimized with .only() to fetch only necessary fields.
    """
    messages_qs = Message.unread.unread_for_user(request.user)
    return render(request, 'unread_messages.html', {'messages': messages_qs})


# -----------------------------------------
# Delete user account (Task 2)
# -----------------------------------------
@login_required
def delete_user(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('home')
    return HttpResponseForbidden("You can only delete your account via POST request")


# -----------------------------------------
# Edit message with history tracking (Task 2)
# -----------------------------------------
@login_required
def edit_message(request, message_id):
    message_obj = get_object_or_404(Message, id=message_id)

    if message_obj.sender != request.user:
        return HttpResponseForbidden("You cannot edit someone else's message")

    if request.method == "POST":
        new_content = request.POST.get('content', '').strip()
        if new_content and new_content != message_obj.content:
            # Save previous content to MessageHistory
            MessageHistory.objects.create(
                message=message_obj,
                old_content=message_obj.content
            )
            # Update message
            message_obj.content = new_content
            message_obj.edited = True
            message_obj.edited_at = timezone.now()
            message_obj.edited_by = request.user
            message_obj.save()

            django_messages.success(request, "Message updated successfully")

        return redirect('message_list')

    return render(request, 'edit_message.html', {'message': message_obj})


# -----------------------------------------
# Recursive function for threaded replies
# -----------------------------------------
def get_threaded_replies(message):
    """
    Recursively get all replies to a message in a threaded format.
    Optimized with select_related for sender.
    """
    replies_list = []
    for reply in message.replies.all().select_related('sender'):
        replies_list.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return replies_list


# -----------------------------------------
# Threaded messages sent by the user (Task 3)
# -----------------------------------------
@login_required
def sent_threaded_messages(request):
    """
    Display messages sent by the logged-in user in threaded format.
    Optimized with select_related and prefetch_related.
    """
    messages_qs = Message.objects.filter(
        sender=request.user,
        parent_message__isnull=True
    ).select_related('receiver').prefetch_related('replies__receiver')

    threaded_messages = []
    for msg in messages_qs:
        threaded_messages.append({
            'message': msg,
            'replies': get_threaded_replies(msg)
        })

    return render(request, 'sent_threaded_messages.html', {'threaded_messages': threaded_messages})
