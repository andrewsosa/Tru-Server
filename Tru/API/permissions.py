from rest_framework.permissions import BasePermission, IsAuthenticated

from API.models import Account

class DefaultFeedPermission(IsAuthenticated):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Admins always have permission
        if request.user.is_staff:
            return True

        # Authors always have all rights
        if obj.author == Account.objects.get(user=request.user.id):
            return True

        # Read permissions are allowed to any friends,
        # so we'll allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            requestee = Account.objects.get(user=request.user.id)
            author = Account.objects.get(user=request.user.id)
            if requestee in author.friends:
                return True

        # No permissions are all
        return False


class DefaultAccountPermission(BasePermission):
    """
    Custom permission to only allow owners or admins to read/edit an account.
    """

    def has_permission(self, request, view):
        return (not request.user.is_anonymous) or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Permissions only granted to owners or admins.
        if request.user.is_staff:
            return True

        return obj.user == request.user.id
