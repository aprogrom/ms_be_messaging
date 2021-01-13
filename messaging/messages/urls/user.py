from django.urls import path, include
from rest_framework.routers import SimpleRouter
from ..views import DialogMessagesViewSet

dialog_messages_router = SimpleRouter()
dialog_messages_router.register(
    'messages', DialogMessagesViewSet, basename='messages',
)

