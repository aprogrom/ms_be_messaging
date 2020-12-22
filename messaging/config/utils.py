import os
from django.core.exceptions import ImproperlyConfigured


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EnviromentVariable(metaclass=Singleton):
    DEBUG = None
    SECRET_KEY = None
    DB_HOST = None
    DB_NAME = None
    DB_USER = None
    DB_PASS = None
    # DB_MAIL_HOST = None
    # DB_MAIL_NAME = None
    # DB_MAIL_USER = None
    # DB_MAIL_PASS = None
    SETTINGS = None
    INSTANCE_TOKEN = None
    API_ENDPOINT_URL = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for variable in self.__get_variables__():
            setattr(self, variable, self.__get_env_variable__(variable))

    def __get_variables__(self):
        return filter(lambda x: x[0] != '_', dir(self))

    @staticmethod
    def __get_env_variable__(var_name):
        try:
            return os.environ[var_name]
        except KeyError:
            error_msg = "Set the {} environment variable".format(var_name)
            raise ImproperlyConfigured(error_msg)