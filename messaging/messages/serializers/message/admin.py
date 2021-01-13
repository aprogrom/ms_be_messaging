import datetime
from django.utils import timezone
from rest_framework.serializers import ModelSerializer, ListSerializer, Serializer, BooleanField, ListField
from rest_framework.fields import CharField
from rest_framework.exceptions import ValidationError
from mscore.serializers.fields import UUIDRemouteRelatedField
from mscore.serializers.base import ManyWithThroughModifySerializer, ThroughRelationSerializer
from relations.models import UserRelationModel
from ...models import Message


# dialog = ForeignKey(to=Dialog, on_delete=CASCADE, related_name='messages')
# text = TextField()
# sent = DateTimeField(auto_now_add=True)
# changed = DateTimeField(auto_now=True)
# answer = ForeignKey(to='self', on_delete=CASCADE, related_name='answers')
# forwarded = ForeignKey(to='self', on_delete=CASCADE, related_name='forwardings')
# requires_answer = BooleanField(default=False)
# is_delete = BooleanField(default=False)

class MessageAdminListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


# class MessageCreateSerializer(ModelSerializer):
#
#     class Meta:
#         model = Message
#         fields = ['text', 'answer', 'forwarded', 'requires_answer']


# class MessageUpdateSerializer(ModelSerializer):
#
#     class Meta:
#         model = Message
#         fields = ['text', 'requires_answer']
#
#     def validate_text(self, value):
#         if timezone.now() > self.instance.sent + datetime.timedelta(minutes=Message.CHANGE_INTERVAL):
#             raise ValidationError(
#                 'Нельзя изменить сообщение если с его отправки прошло больше {} минут'.format(
#                     Message.CHANGE_INTERVAL
#                 )
#             )
#         return value


class MessageDeleteSerializer(ModelSerializer):

    class Meta:
        model = Message
        fields = ['is_delete',]

    def validate_is_delete(self, value):
        if timezone.now() > self.instance.sent + datetime.timedelta(minutes=Message.DELETE_INTERVAL):
            raise ValidationError(
                'Нельзя удалить/востановить сообщение если с его отправки прошло более {} минут'.format(
                    Message.DELETE_INTERVAL
                )
            )
        if self.instance.is_delete == value:
            raise ValidationError('Нельзя повторно совершить одно и то же действие')
        return value
