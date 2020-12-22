from rest_framework.serializers import ModelSerializer, BooleanField
from rest_framework.exceptions import ValidationError
from mscore.serializers.fields import UUIDRemouteRelatedField
from mscore.serializers.base import ManyWithThroughModifySerializer, ThroughRelationSerializer
from relations.models import UserRelationModel
from ..models import Dialog, UserDialog
from .user_dialog import UserDialogSerializer

# name = CharField(max_length=250)
# users_count = IntegerField(default=0)
# is_private = BooleanField()
# is_group = BooleanField()
# is_educational = BooleanField()
# deleted = DateTimeField(null=True, blank=True)
# is_delete = BooleanField(default=False)


# class UserDialogSerializer(ThroughRelationSerializer, ModelSerializer):
#     user = UUIDRemouteRelatedField(queryset=UserRelationModel.objects.all(), return_uid=True)
#     admin = BooleanField(default=False, required=False)
#
#     class Meta:
#         model = UserDialog
#         fields = ['user', 'admin']
#         through_fields = ('dialog', 'user')


class DialogAdminListSerializer(ModelSerializer):

    class Meta:
        model = Dialog
        fields = '__all__'
        read_only_fields = ['name', 'users_count', 'is_private', 'is_group', 'is_educational', 'deleted', 'is_delete']


class DialogAdminDetailSerializer(DialogAdminListSerializer):
    users = UserDialogSerializer(many=True, read_only=True)


class DialogAdminCreateSerializer(ManyWithThroughModifySerializer):
    users = UserDialogSerializer(many=True, read_only=True)

    class ERRORS:
        class TYPE:
            NEED_ANYONE = 'Необходимо выбрать тип диалога'
            NEED_ONLY_ONE = 'Необходимо выбрать только один тип диалога'
        class IS_PRIVATE:
            ONLY_TWO = 'Личный диалог создается только между двумя пользователями'
        class IS_GROUP:
            ONLY_MORE_TWO = 'Групповой диалог создается только между более чем двумя пользователями'
        class USERS:
            ONLY_ONE = 'Нельзя создать диалог с 1 пользователем.'
            NEED_OWNER = 'Необходим хотя бы 1 владелец диалога.'

    class Meta:
        model = Dialog
        fields = ['users', 'is_private', 'is_group', 'is_educational']
        many = {
            'users': UserDialogSerializer,
        }

    def validate_users(self, value):
        value = list(map(dict, set(tuple(sorted(x.items())) for x in value)))
        if len(value) == 1:
            raise ValidationError(self.ERRORS.USERS.ONLY_ONE)
        owners = [el['user'] for el in value if el['admin']]
        if len(owners) == 0:
            raise ValidationError(self.ERRORS.USERS.NEED_OWNER)
        return value

    def validate_is_private(self, value):
        users = list(map(dict, set(tuple(sorted(x.items())) for x in self.initial_data['users'])))
        if value and len(users) != 2:
            raise ValidationError(self.ERRORS.IS_PRIVATE.ONLY_TWO)
        return value

    def validate_is_group(self, value):
        users = list(map(dict, set(tuple(sorted(x.items())) for x in self.initial_data['users'])))
        if value and len(users) < 3:
            raise ValidationError(self.ERRORS.IS_GROUP.ONLY_MORE_TWO)
        return value

    def validate(self, attrs):
        errors = {}
        def append_error(key, msg):
            if key in errors:
                errors[key].append(msg)
            else:
                errors[key] = [msg]
        if not attrs['is_private'] and not attrs['is_group'] and  not attrs['is_educational']:
            append_error('is_private', self.ERRORS.TYPE.NEED_ANYONE)
            append_error('is_group', self.ERRORS.TYPE.NEED_ANYONE)
            append_error('is_educational', self.ERRORS.TYPE.NEED_ANYONE)
        if (attrs['is_private'] and attrs['is_group']) or \
                (attrs['is_group'] and attrs['is_educational']) or \
                (attrs['is_private'] and attrs['is_educational']):
            append_error('is_private', self.ERRORS.TYPE.NEED_ONLY_ONE)
            append_error('is_group', self.ERRORS.TYPE.NEED_ONLY_ONE)
            append_error('is_educational', self.ERRORS.TYPE.NEED_ONLY_ONE)
        if len(errors.keys()) > 0:
            raise ValidationError(errors)
        if attrs['is_private']:
            for user in attrs['users']:
                user['owner'] = True
        return attrs


class DialogAdminChangeUsersSerializer(ManyWithThroughModifySerializer):
    users = UserDialogSerializer(many=True, read_only=True)

    class ERRORS:
        class TYPE:
            NEED_ANYONE = 'Необходимо выбрать тип диалога'
            NEED_ONLY_ONE = 'Необходимо выбрать только один тип диалога'
        class IS_PRIVATE:
            ONLY_TWO = 'Личный диалог создается только между двумя пользователями'
        class IS_GROUP:
            ONLY_MORE_TWO = 'Групповой диалог создается только между более чем двумя пользователями'
        class USERS:
            ONLY_ONE = 'Нельзя создать диалог с 1 пользователем.'

    class Meta:
        model = Dialog
        fields = ['users']
        many = {
            'users': UserDialogSerializer
        }

    def validate_users(self, value):
        if self.instance.is_private:
            raise ValidationError('Добавлять пользователей в личный диалог нельзя')
        return value
