from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants in a conversation can view, create, update, or delete messages
    """

    def has_permission(self, request, view):
        # Only authenticated users
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow participants to view, edit, delete
        if hasattr(obj, 'participants'):  # Conversation
            participants = obj.participants.all()
        elif hasattr(obj, 'conversation'):  # Message
            participants = obj.conversation.participants.all()
        else:
            return False

        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return request.user in participants
        elif request.method in ["PUT", "PATCH", "DELETE", "POST"]:
            return request.user in participants
        return False
