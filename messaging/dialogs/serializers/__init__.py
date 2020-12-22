from .admin import DialogAdminListSerializer, DialogAdminDetailSerializer, \
    DialogAdminChangeUsersSerializer, DialogAdminCreateSerializer

from .user import DialogListSerializer, DialogDetailSerializer, DialogRenameSerializer, PrivateDialogCreateSerializer, \
    GroupDialogCreateSerializer

from .user_dialog import UserDialogSerializer, UserDialogChangeSerializer, UserDialogRemoveSerializer, \
    UserDialogChangeListSerializer, UserDialogRemoveListSerializer