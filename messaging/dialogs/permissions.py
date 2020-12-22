from rest_framework.permissions import BasePermission


class DialogAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.users.filter(user=request.user.db_user).admin:
            return True
        return False

    def has_permission(self, request, view):
        return True
