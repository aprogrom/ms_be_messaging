from rest_framework.serializers import ModelSerializer, ListSerializer, Serializer, BooleanField, ListField
from rest_framework.fields import CharField
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

class ERRORS:
    class TYPE:
        NEED_ANYONE = 'Необходимо выбрать тип диалога'
        NEED_ONLY_ONE = 'Необходимо выбрать только один тип диалога'

    class IS_PRIVATE:
        ONLY_TWO = 'Личный диалог создается только между двумя пользователями'

    class IS_GROUP:
        ONLY_MORE_TWO = 'Групповой диалог создается только между более чем двумя пользователями'

    class USERS:
        WITH_SELF = 'Нельзя создать диалог только с собой'
        ONLY_ONE = 'Нельзя создать диалог с 1 пользователем.'
        NEED_OWNER = 'Необходим хотя бы 1 владелец диалога.'




class DialogListSerializer(ModelSerializer):

    class Meta:
        model = Dialog
        fields = ['id', 'name', 'users_count', 'is_private', 'is_group', 'is_educational']
        read_only_fields = ['id', 'name', 'users_count', 'is_private', 'is_group', 'is_educational']


class DialogDetailSerializer(DialogListSerializer):
    users = UserDialogSerializer(many=True, read_only=True)

    class Meta:
        model = Dialog
        fields = ['id', 'name', 'users', 'users_count', 'is_private', 'is_group', 'is_educational']
        read_only_fields = ['id', 'name', 'users', 'users_count', 'is_private', 'is_group', 'is_educational']


class PrivateDialogCreateSerializer(ModelSerializer):
    user = UUIDRemouteRelatedField(queryset=UserRelationModel.objects.all())
    name = CharField(max_length=250, required=False, allow_null=False, allow_blank=False)
    ERRORS = ERRORS

    class Meta:
        model = Dialog
        fields = ['user', 'name']

    def validate_user(self, value):
        print(value)
        if self.context['request'].user.db_user == value:
            raise ValidationError(self.ERRORS.USERS.WITH_SELF)
        return value

    def validate(self, attrs):
        if 'name' not in attrs or attrs['name'] == '' or attrs['name'] is None:
            print(attrs)
            attrs['name'] = f"{self.context['request'].user.db_user.short_name}, {attrs['user'].short_name}"
        return attrs

    def create(self, validated_data):
        validated_data['is_private'] = True
        validated_data['is_group'] = False
        validated_data['is_educational'] = False
        print(validated_data)
        user = validated_data.pop('user')
        instance = super(PrivateDialogCreateSerializer, self).create(validated_data)
        instance.users.create(dialog=instance, user=self.context['request'].user.db_user, admin=True)
        instance.users.create(dialog=instance, user=user, admin=True)
        return instance


class GroupDialogCreateSerializer(ManyWithThroughModifySerializer):
    users = UserDialogSerializer(many=True)
    name = CharField(max_length=250, required=False, allow_null=False, allow_blank=False)
    ERRORS = ERRORS

    class Meta:
        model = Dialog
        fields = ['users', 'name']
        many = {
            'users': UserDialogSerializer,
        }

    def validate_users(self, value):
        users = [el for el in value if el['user'] != self.context['request'].user.db_user]
        if len(users) == 1:
            raise ValidationError(self.ERRORS.USERS.ONLY_ONE)
        return users

    def validate(self, attrs):
        if 'name' not in attrs or attrs['name'] == '' or attrs['name'] is None:
            print(attrs)
            names = []
            names.append(
                self.context['request'].user.db_user.short_name
            )
            for user in attrs['users']:
                names.append(
                    user['user'].short_name
                )
            attrs['name'] = ', '.join(names)
        return attrs

    def create(self, validated_data):
        validated_data['is_private'] = False
        validated_data['is_group'] = True
        validated_data['is_educational'] = False
        users = validated_data.pop('users')
        return super().create(validated_data)


class DialogRenameSerializer(ModelSerializer):

    class Meta:
        model = Dialog
        fields = ['name']

