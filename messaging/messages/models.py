from django.db.models import Model, CharField, IntegerField, BooleanField, ForeignKey, DateTimeField, TextField
from django.db.models.deletion import CASCADE
from mscore.models.basemodels import UUIDBaseModel
from relations.models import UserRelationModel
from dialogs.models import Dialog


class Message(UUIDBaseModel):
    dialog = ForeignKey(to=Dialog, on_delete=CASCADE, related_name='messages')
    text = TextField()
    sent = DateTimeField(auto_now_add=True)
    changed = DateTimeField(auto_now=True)
    answer = ForeignKey(to='self', on_delete=CASCADE, related_name='answers')
    forwarded = ForeignKey(to='self', on_delete=CASCADE, related_name='forwardings')
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

