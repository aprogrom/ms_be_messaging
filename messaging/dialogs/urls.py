from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import DialogAdminViewSet, DialogViewSet


app_name = 'dialogs'

dialog_router = SimpleRouter()
dialog_router.register(
    'dialogs', DialogViewSet, basename='dialogs',
)

admin_dialog_router = SimpleRouter()
admin_dialog_router.register(
    'dialogs', DialogAdminViewSet, basename='dialogs',
)


urlpatterns = [
    path('admin/', include((admin_dialog_router.urls, 'local_admin'), namespace='admin')),
    path('', include((dialog_router.urls, 'self'), namespace='self'))
]
