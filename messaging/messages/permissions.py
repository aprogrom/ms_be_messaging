from rest_framework.permissions import BasePermission
from .models import Message


class IsOwnMessagePermission(BasePermission):
    def has_object_permission(self, request, view, obj: Message):
        if obj.user == request.user.db_user:
            return True
        return False

    def has_permission(self, request, view):
        return True
