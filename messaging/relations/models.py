# import requests
# from django.conf import settings
# from mscore.constants import APIENDPOINT_URLS
# from django.db.models import BooleanField, OneToOneField, CASCADE, Model
from mscore.models import RelationBaseModel, RelationSpecificModelBaseManager


class UserRelationManager(RelationSpecificModelBaseManager):
    related_model = 'accounts.users.user'


class UserRelationModel(RelationBaseModel):
    objects = UserRelationManager()

    @property
    def is_superuser(self):
        self.load_user_object()
        return self._user['is_superuser']

    @property
    def is_student(self):
        self.load_user_object()
        return self._user['is_student']

    @property
    def is_employee(self):
        self.load_user_object()
        return self._user['is_employee']

    @property
    def lastname(self):
        self.load_user_object()
        return self._user['lastname']

    @property
    def firstname(self):
        self.load_user_object()
        return self._user['firstname']

    @property
    def midname(self):
        self.load_user_object()
        return self._user['midname']

    @property
    def short_name(self):
        self.load_user_object()
        if self._user["firstname"] == "":
            return f'{self._user["lastname"]}'
        if self._user["midname"] == "":
            return f'{self._user["firstname"][0]}.{self._user["lastname"]}'
        return f'{self._user["firstname"][0]}.{self._user["midname"][0]}.{self._user["lastname"]}'

    def load_user_object(self):
        if not hasattr(self, '_user'):
            fields = [
                'is_superuser',
                'username',
                'lastname',
                'firstname',
                'midname',
                'is_student',
                'is_employee',
            ]
            data = self.get_related_data(fields)
            for field in fields:
                if field not in data:
                    data[field] = ''
            self._user = {
                'username': data['username'],
                'lastname': data['lastname'],
                'firstname': data['firstname'],
                'midname': data['midname'],
                'is_superuser': bool(data['is_superuser']) if 'is_superuser' in data else False,
                'is_student': bool(data['is_student']) if 'is_student' in data else False,
                'is_employee': bool(data['is_employee']) if 'is_employee' in data else False,
            }

    # @property
    # def is_head(self):
    #     self.load_worker_object()
    #     return self._worker['position']['head']

    # @property
    # def is_local_admin(self):
    #     """
    #     Проверяем, имеет ли работник роль локального администратора
    #     :return: bool
    #     """
    #     if hasattr(self, 'additionworkerinfomodel'):
    #         return self.additionworkerinfomodel.is_local_admin
    #     return False


# class AdditionWorkerInfoModel(Model):
#     worker = OneToOneField(to=WorkerRelationModel, on_delete=CASCADE)
#     is_local_admin = BooleanField(default=True)
#
#
# class DepartmentRelationManager(RelationSpecificModelBaseManager):
#     related_model = 'organization.department.department'
#
#
# class DepartmentRelationModel(RelationBaseModel):
#     objects = DepartmentRelationManager()

