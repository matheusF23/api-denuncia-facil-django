from rest_framework import permissions


class UpdateOwnUser(permissions.BasePermission):
    """Allow user to edit their own account"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
