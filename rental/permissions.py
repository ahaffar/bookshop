from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


class UserUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class UserProfileOwnerUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class UserViewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('rental.view_user'):
            return True
        return False


class GroupPermissions(permissions.BasePermission):
    message = 'you are not authorized to access this view - please contact administrator'
    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_superuser
        return Response({'detail': self.message}, status=status.HTTP_403_FORBIDDEN)
