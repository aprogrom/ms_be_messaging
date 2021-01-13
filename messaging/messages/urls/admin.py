from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ..views import DialogMessagesAdminViewSet

admin_dialog_messages_router = SimpleRouter()
admin_dialog_messages_router.register(
    'messages', DialogMessagesAdminViewSet, basename='messages',
)

