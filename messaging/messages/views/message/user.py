from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK, HTTP_205_RESET_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from mscore.viewsets import MultiSerializerViewSet
from mscore.constants import ACTIONS
from mscore.permissions import IsGlobalAdminPermission
from dialogs.views import ByDialogBaseMixin
from dialogs.permissions import InDialogPermission
from ...models import Message, Dialog
from ...serializers import MessageListSerializer, MessageCreateSerializer, MessageUpdateSerializer, \
    MessageDeleteSerializer, MessageAnswersDetailSerializer




class DialogMessagesViewSet(
                        ByDialogBaseMixin,
                        MultiSerializerViewSet,
                        CreateModelMixin,
                        RetrieveModelMixin,
                        UpdateModelMixin,
                        DestroyModelMixin,
                        ListModelMixin,
                        GenericViewSet
    ):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
    serializers_class = {
        ACTIONS.LIST: MessageListSerializer,
        ACTIONS.RETRIEVE: MessageAnswersDetailSerializer,
        ACTIONS.POST: MessageCreateSerializer,
        ACTIONS.PUT: MessageUpdateSerializer,
        ACTIONS.DELETE: MessageDeleteSerializer,
    }
    permission_classes = [InDialogPermission,]

    # def get_permissions(self):
    #     if self.action in [
    #         ACTIONS.PUT,
    #         'append_user_action',
    #         'remove_user_action',
    #         'change_user_status_action',
    #     ]:
    #         return [DialogAdminPermission(),]
    #     return []

    def get_queryset(self):
        qs = super().get_queryset().filter(dialog__id=self.get_dialog_pk())
        if self.request.method != 'DELETE':
            qs = qs.filter(is_delete=False)
        return qs

    def perform_create(self, serializer: MessageCreateSerializer):
        serializer.save(user=self.request.user.db_user, dialog=self.get_dialog())

    def perform_update(self, serializer):
        serializer.save(is_changed=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'is_delete': not instance.is_delete})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT if instance.is_delete else HTTP_205_RESET_CONTENT)



