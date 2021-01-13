from rest_framework.permissions import BasePermission


class DialogAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = obj.users.filter(user=request.user.db_user).first()
        if user and user.admin:
            return True
        return False

    def has_permission(self, request, view):
        return True


class InDialogPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

    def has_permission(self, request, view):
        dialog = view.get_dialog()
        if dialog.users.filter(user=request.user.db_user).count() > 0:
            return True
        return False