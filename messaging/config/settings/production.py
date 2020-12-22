from .base import *

ALLOWED_HOSTS = ['127.0.0.1', ]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticmedia", "static")

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticmedia", "media")

STATICFILES_DIRS = [
   # os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
