from django.utils import timezone
from django.db.models import Model, CharField, IntegerField, BooleanField, ForeignKey, DateTimeField
from django.db.models.deletion import CASCADE
from mscore.models.basemodels import UUIDBaseModel
from relations.models import UserRelationModel


class Dialog(UUIDBaseModel):
    name = CharField(max_length=250)
    users_count = IntegerField(default=0)
    is_private = BooleanField()
    is_group = BooleanField()
    is_educational = BooleanField()
    deleted = DateTimeField(null=True, blank=True)
    is_delete = BooleanField(default=False)

    def delete(self, force=False, **kwargs):
        if force:
            super().delete(**kwargs)
        elif not self.is_delete:
            self.deleted = timezone.now()
            self.is_delete = True
            self.save(update_fields=['deleted', 'is_delete'])

    def restore(self):
        if self.is_delete:
            self.deleted = timezone.now()
            self.is_delete = True
            self.save(update_fields=['deleted', 'is_delete'])

    def append_users(self, users):
        dialog_users = []
        existed = [exist.user for exist in self.users.filter(user__in=users)]
        for user in users:
            if user not in existed:
                dialog_users.append(self.users.model(dialog=self, user=user))
        return self.users.bulk_create(dialog_users)

    def append_user(self, user: UserRelationModel, admin=False):
        if self.users.filter(user=user).count() == 0:
            self.users.create(dialog=self, user=user, admin=admin)
            return True
        else:
            return False

    def remove_user(self, user: UserRelationModel):
        users = self.users.filter(user=user)
        count = users.count()
        if count > 0:
            users.delete()
            return True
        else:
            return False

    def is_user_in_dialog(self, user: UserRelationModel):
        if self.users.filter(user=user) > 0:
            return True
        else:
            return False

    def make_name(self):
        names = []
        for user in self.users.all():
            names.append(
                user.user.short_name
            )
        return ', '.join(names)

class UserDialog(Model):
    dialog = ForeignKey(to=Dialog, on_delete=CASCADE, related_name='users')
    user = ForeignKey(to=UserRelationModel, on_delete=CASCADE, related_name='dialogs')
    admin = BooleanField(default=False)
    unread = IntegerField(default=0)
