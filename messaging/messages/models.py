from django.db.models import Model, CharField, IntegerField, BooleanField, ForeignKey, DateTimeField, TextField
from django.db.models.deletion import CASCADE, SET_NULL
from mscore.models.basemodels import UUIDBaseModel
from relations.models import UserRelationModel
from dialogs.models import Dialog


class Message(UUIDBaseModel):
    DELETE_INTERVAL = 15
    CHANGE_INTERVAL = 30

    dialog = ForeignKey(to=Dialog, on_delete=CASCADE, related_name='messages')
    user = ForeignKey(to=UserRelationModel, on_delete=SET_NULL, related_name='messages', null=True)
    text = TextField()
    sent = DateTimeField(auto_now_add=True)
    is_changed = BooleanField(default=False)
    changed = DateTimeField(auto_now=True)
    answer = ForeignKey(to='self', on_delete=CASCADE, related_name='answers', null=True, blank=True, default=None)
    forwarded = ForeignKey(to='self', on_delete=CASCADE, related_name='forwardings', null=True, blank=True, default=None)
    requires_answer = BooleanField(default=False)
    is_delete = BooleanField(default=False)


class ReadMessage(Model):
    message = ForeignKey(to=Message, on_delete=CASCADE, related_name='readers')
    user = ForeignKey(to=UserRelationModel, on_delete=CASCADE, related_name='read_messages')
    read = DateTimeField(null=True, blank=True)


class Reference(Model):
    message = ForeignKey(to=Message, on_delete=CASCADE, related_name='references')
    refer = ForeignKey(to=UserRelationModel, on_delete=CASCADE, related_name='referenced')
    is_react = BooleanField(default=False)
    reacted = DateTimeField(null=True, blank=True)

