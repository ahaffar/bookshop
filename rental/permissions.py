from rest_framework import permissions


class UserUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


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

