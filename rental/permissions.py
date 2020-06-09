from rest_framework import permissions, exceptions
import copy


# def has_perm(user):
#     return user.groups.filter(name__in=['librarians', ]).exists()

PERMS_MAP = {
    'GET': 'view_',
    'DELETE': 'delete_',
    'PATCH': 'change_',
    'POST': 'add_',
    'PUT': 'change_'
}


class UserUpdatePermission(permissions.BasePermission):
    """
    This is for the /bookshop/user/ API
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class UserProfileOwnerUpdate(permissions.BasePermission):
    """
    this is for /bookshop/bio/ API
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


# MODEL_NAME = 'user'
# CRUD_OPS = ['change', 'delete', 'add', 'view']
#
#
# def perms_check(user, model, app, *args):
#     perms_list = list(user.get_all_permissions())
#     for count, perm in enumerate(*args):
#         if '%s.%s_%s' % (app, perm, model) in perms_list:
#             return True
#         return False


class UserViewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        app_label = view.queryset.model._meta.app_label
        model_name = view.queryset.model._meta.model_name

        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return request.user.is_admin() or request.user.is_superuser
        elif request.method in ('PUT', 'PATCH'):
            return request.user.has_perm(str(app_label+'.'+PERMS_MAP[request.method]+model_name)) or \
                   request.user.is_superuser
        elif request.method == 'DELETE':
            return request.user.has_perm(str(app_label+'.'+PERMS_MAP[request.method]+model_name)) or \
                   request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or \
               request.user.is_admin() or request.user.is_superuser

