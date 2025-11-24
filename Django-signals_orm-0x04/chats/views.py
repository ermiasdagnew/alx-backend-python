from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages as django_messages
from messaging.models import Message, MessageHistory

# -----------------------------------------
# List messages for logged-in user
# -----------------------------------------
@login_required
@cache_page(60)  # cache for 60 seconds
def message_list(request):
    messages_qs = Message.objects.filter(
        receiver=request.user
    ).select_related('sender', 'parent_message').prefetch_related('replies')[:50]

    return render(request, 'messages.html', {'messages': messages_qs})


# -----------------------------------------
# Delete user account (Task 2 requirement)
# -----------------------------------------
@login_required
def delete_user(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        return redirect('home')  # redirect after deletion
    return HttpResponseForbidden("You can only delete your account via POST request")


# -----------------------------------------
# Edit message with history tracking
# -----------------------------------------
@login_required
def edit_message(request, message_id):
    message_obj = get_object_or_404(Message, id=message_id)

    # Only the sender can edit their message
    if message_obj.sender != request.user:
        return HttpResponseForbidden("You cannot edit someone else's message")

    if request.method == "POST":
        new_content = request.POST.get('content', '').strip()
        if new_content and new_content != message_obj.content:
            # Save old content in history
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

