from rest_framework.viewsets import ReadOnlyModelViewSet
# from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK
from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
from mscore.viewsets import MultiSerializerViewSet
from mscore.constants import ACTIONS
from mscore.permissions import IsGlobalAdminPermission
from dialogs.views import ByDialogBaseMixin
from ...models import Message, Dialog
from ...serializers import MessageAdminListSerializer


class DialogMessagesAdminViewSet(ByDialogBaseMixin, MultiSerializerViewSet, ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageAdminListSerializer
    # serializers_class = {
    #     ACTIONS.LIST: DialogAdminListSerializer,
    #     ACTIONS.RETRIEVE: DialogAdminDetailSerializer,
    #     ACTIONS.POST: DialogAdminCreateSerializer,
    #     ACTIONS.PATCH: DialogAdminChangeUsersSerializer,
    # }
    permission_classes = [IsGlobalAdminPermission,]

    # def get_dialog_pk(self):
    #     return self.kwargs['dialog']
    #
    # def get_dialog(self):
    #     return Dialog.objects.get(id=self.get_dialog_pk())

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(dialog__id=self.get_dialog_pk())

    # def update(self, request, *args, **kwargs):
    #     if self.action == ACTIONS.PUT:
    #         return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
    #     return super().update(request, *args, **kwargs)

    # @action(methods=['DELETE'], url_name='force_delete', url_path='force', detail=True)
    # def force_delete(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete(force=True)
    #     return Response(status=HTTP_204_NO_CONTENT)
