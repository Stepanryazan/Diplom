from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Check if the user is the owner of an object"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False