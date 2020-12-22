from django.db.models import Model, CharField, IntegerField, BooleanField, ForeignKey, DateTimeField, FloatField, FileField
from django.db.models.deletion import CASCADE
from messages.models import Message


def file_path(instance, filename):
    return f'{instance.message.dialog.uid}/messages/{instance.message.id}/files/{filename}'


class File(Model):
    # FILE_TYPES = (
    #     ('Document', 'PDF'),
    #     ('Audio', 'PDF'),
    #     ('Video', 'PDF'),
    # )

    message = ForeignKey(to=Message, on_delete=CASCADE, related_name='files')
    file = FileField(upload_to=file_path)
    size = FloatField()
    uploaded = DateTimeField(auto_now_add=True)
    # type = CharField(max_length=10)


