from django.urls import path, include
from .admin import admin_dialog_messages_router
from .user import dialog_messages_router



app_name = 'messages'

urlpatterns = [
    path('admin/dialogs/<int:dialog>/', include((admin_dialog_messages_router.urls, 'local_admin'), namespace='admin')),
    path('dialogs/<int:dialog>/', include((dialog_messages_router.urls, 'self'), namespace='self')),
]
