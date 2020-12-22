from rest_framework.serializers import ModelSerializer, BooleanField, Serializer
from mscore.serializers.fields import UUIDRemouteRelatedField
from mscore.serializers.base import ThroughRelationSerializer
from relations.models import UserRelationModel
from ..models import UserDialog


class UserDialogSerializer(ThroughRelationSerializer, ModelSerializer):
    user = UUIDRemouteRelatedField(queryset=UserRelationModel.objects.all(), return_uid=True)
    admin = BooleanField(default=False, required=False)

    class Meta:
        model = UserDialog
        fields = ['user', 'admin']
        through_fields = ('dialog', 'user')


class UserDialogChangeSerializer(ModelSerializer):
    user = UUIDRemouteRelatedField(queryset=UserRelationModel.objects.all(), return_uid=True)
    admin = BooleanField(default=False, required=False)

    class Meta:
        model = UserDialog
        fields = ['user', 'admin']


class UserDialogRemoveSerializer(ModelSerializer):
    user = UUIDRemouteRelatedField(queryset=UserRelationModel.objects.all(), return_uid=True)

    class Meta:
        model = UserDialog
        fields = ['user',]


class UserDialogChangeListSerializer(Serializer):
    users = UserDialogChangeSerializer(many=True)


class UserDialogRemoveListSerializer(Serializer):
    users = UserDialogRemoveSerializer(many=True)