from rest_framework.permissions import BasePermission


class IsGlobalAdminPermission(BasePermission):

    def has_permission(self, request, view):
        if hasattr(request.user, 'is_superuser'):
            return request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'is_superuser'):
            return request.user.is_superuser
        return False


class IsLocalAdmin(BasePermission):
    def has_permission(self, request, view):
        request.user.is_local_admin = request.user.db_user.is_local_admin
        return True if request.user.is_local_admin else False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsHeadPosition(BasePermission):

    def has_permission(self, request, view):
        return True if request.user.db_user and request.user.db_user.is_head else False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)