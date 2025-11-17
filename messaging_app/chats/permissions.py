from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # If object has 'user' field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # If object has 'participants' ManyToMany field
        elif hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        return False
