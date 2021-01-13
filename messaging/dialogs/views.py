from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from mscore.viewsets import MultiSerializerViewSet
from mscore.constants import ACTIONS
from mscore.permissions import IsGlobalAdminPermission
from .models import Dialog
from .serializers import DialogAdminListSerializer, DialogAdminDetailSerializer, DialogAdminCreateSerializer, \
    DialogAdminChangeUsersSerializer, DialogListSerializer, DialogDetailSerializer, DialogRenameSerializer, \
    GroupDialogCreateSerializer, PrivateDialogCreateSerializer, UserDialogChangeListSerializer, UserDialogRemoveListSerializer
from .permissions import DialogAdminPermission


class DialogAdminViewSet(MultiSerializerViewSet, ModelViewSet):
    queryset = Dialog.objects.all()
    serializer_class = DialogAdminListSerializer
    serializers_class = {
        ACTIONS.LIST: DialogAdminListSerializer,
        ACTIONS.RETRIEVE: DialogAdminDetailSerializer,
        ACTIONS.POST: DialogAdminCreateSerializer,
        ACTIONS.PATCH: DialogAdminChangeUsersSerializer,
    }
    permission_classes = [IsGlobalAdminPermission(),]

    def update(self, request, *args, **kwargs):
        if self.action == ACTIONS.PUT:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(methods=['DELETE'], url_name='force_delete', url_path='force', detail=True)
    def force_delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete(force=True)
        return Response(status=HTTP_204_NO_CONTENT)


class DialogViewSet(
                        MultiSerializerViewSet,
                        # CreateModelMixin,
                        RetrieveModelMixin,
                        # UpdateModelMixin,
                        DestroyModelMixin,
                        ListModelMixin,
                        GenericViewSet
    ):
    queryset = Dialog.objects.all()
    serializer_class = DialogListSerializer
    serializers_class = {
        ACTIONS.LIST: DialogListSerializer,
        ACTIONS.RETRIEVE: DialogDetailSerializer,
        'create_private_action': PrivateDialogCreateSerializer,
        'create_group_action': GroupDialogCreateSerializer,
        ACTIONS.PUT: DialogRenameSerializer,
        'append_user_action': UserDialogChangeListSerializer,
        'remove_user_action': UserDialogRemoveListSerializer,
        'change_user_status_action': UserDialogChangeListSerializer,
    }
    permission_classes = [DialogAdminPermission(),]

    def get_permissions(self):
        if self.action in [
            ACTIONS.PUT,
            'append_user_action',
            'remove_user_action',
            'change_user_status_action',
        ]:
            return [DialogAdminPermission(),]
        return []

    def get_queryset(self):
        return super().get_queryset().filter(users__user=self.request.user.db_user)

    def perform(self, request, create=True, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, instance=None if create else self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        detail_serializer = DialogDetailSerializer(instance=serializer.instance)
        return Response(detail_serializer.data, status=HTTP_201_CREATED if create else HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='private', url_name='create_private')
    def create_private_action(self, request, *args, **kwargs):
        return self.perform(request, *args, **kwargs)

    @action(methods=['POST'], detail=False, url_path='group', url_name='create_group')
    def create_group_action(self, request, *args, **kwargs):
        return self.perform(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.perform(request, *args, create=False, **kwargs)

    @action(methods=['PUT'], detail=True, url_path='users/append', url_name='append_user')
    def append_user_action(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance: Dialog = self.get_object()
        dialog_users = [el.user for el in instance.users.all()]
        new = []
        users = []
        for el in serializer.validated_data['users']:
            if el not in new and el['user'] not in dialog_users:
                new.append(el)
                users.append(instance.users.model(
                    dialog=instance,
                    user=el['user'],
                    admin=el['admin']
                ))
        # users = [el for el in serializer.validated_data['users'] if el['user'] not in dialog_users]
        instance.users.bulk_create(users)
        instance.name = instance.make_name()
        instance.save()
        detail_serializer = DialogDetailSerializer(instance=instance)
        return Response(detail_serializer.data, status=HTTP_200_OK)
        # return self.perform(request, *args, append_data={'dialog': self.get_object()}, create=False, **kwargs)

    @action(methods=['DELETE'], detail=True, url_path='users/remove', url_name='remove_user')
    def remove_user_action(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance: Dialog = self.get_object()
        users = [el['user'] for el in serializer.validated_data['users'] if el['user'] != self.request.user.db_user]
        dialog_users = instance.users.filter(user__in=users)
        if instance.users.count() - dialog_users.count() <= 2:
            raise ValidationError({'detail': 'Групповой диалог менее чем на 3 челвоек не имеет смысл, ' +
                                             'если он вам более не актуален, расформируйте его.'})
        dialog_users.delete()
        instance.name = instance.make_name()
        instance.save()
        detail_serializer = DialogDetailSerializer(instance=instance)
        return Response(detail_serializer.data, status=HTTP_200_OK)
        # return self.perform(request, *args, append_data={'dialog': self.get_object()}, create=False, **kwargs)

    @action(methods=['PATCH'], detail=True, url_path='users/change', url_name='change_user_status_action')
    def change_user_status_action(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance: Dialog = self.get_object()
        users = [el['user'] for el in serializer.validated_data['users'] if el['user'] != self.request.user.db_user]
        dialog_users = instance.users.filter(user__in=users)
        # print(self.request.user.db_user.uid)
        for changes in serializer.validated_data['users']:
            user = next((el for el in dialog_users if el.user == changes['user']), None)
            # print(user)
            if user is not None:# and user.user != self.request.user.db_user:
                user.admin = changes['admin']
        instance.users.bulk_update(dialog_users, ['admin'])
        # if instance.users.count() - dialog_users.count() <= 2:
        #     raise ValidationError({'detail': 'Групповой диалог менее чем на 3 челвоек не имеет смысл, ' +
        #                                      'если он вам более не актуален, расформируйте его.'})
        # dialog_users.delete()
        detail_serializer = DialogDetailSerializer(instance=instance)
        return Response(detail_serializer.data, status=HTTP_200_OK)


class ByDialogBaseMixin:
    def get_dialog_pk(self):
        return self.kwargs['dialog']

    def get_dialog(self):
        return Dialog.objects.get(id=self.get_dialog_pk())
