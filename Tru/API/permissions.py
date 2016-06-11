from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework import permissions
from API.models import Account

class UserPermission(BasePermission):
    """
    Custom permission that allows anon users to only POST (register), but
    denys other actions. Other non-admin users only have permissions to
    read from their own account. See the UserViewSet to see how handling
    is done for authenicated users.
    """

    def has_permission(self, request, view):
        # Allow anonymous users to register only via POST
        if request.user.is_anonymous():
            if request.method == "POST":
                return True
            else:
                return False

        # Allow staff all permissions
        if request.user.is_staff:
            return True

        # Allow users to access own data?
        return True

    def has_object_permission(self, request, view, obj):
        # Admins always have permission
        if request.user.is_staff:
            return True

        # Owners always have rights
        if obj == request.user:
            return True

        return False


class AccountPermission(IsAuthenticated):
    """
    Custom permission to only allow owners or admins to read/edit an account.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return IsAuthenticated.has_permission(self, request, view)

    def has_object_permission(self, request, view, obj):
        # Permissions only granted to owners or admins.
        if request.user.is_staff:
            return True

        return obj.user == request.user


class FeedPermission(IsAuthenticated):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return IsAuthenticated.has_permission(self, request, view)

    def has_object_permission(self, request, view, obj):
        # Admins always have permission
        if request.user.is_staff:
            return True

        # Read permissions are allowed to any friends,
        # so we'll allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:

            return True # temp

            requestee = Account.objects.get(user=request.user)
            author = Account.objects.get(user=request.user)
            if requestee in author.friends:
                return True

        # Authors always have all rights
        if obj.author == Account.objects.get(user=request.user.id):
            return True

        # No permissions are all
        return False
