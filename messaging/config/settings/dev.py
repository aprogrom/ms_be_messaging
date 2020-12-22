from .base import *

ALLOWED_HOSTS = ['193.232.56.4', ]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticmedia", "static")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticmedia", "media")

STATICFILES_DIRS = [
   # os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'

API_END_POINT_URL = EVARS.API_ENDPOINT_URL

API_TOKEN = EVARS.INSTANCE_TOKEN