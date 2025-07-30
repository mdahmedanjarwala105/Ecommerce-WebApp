from .common import *

DEBUG = True

SECRET_KEY = "django-insecure-bhvlja&8qr-_6k3)dqbxb1fn#h=_$fxs-#q@jxl$sah(7_!#v1"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASS"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}
