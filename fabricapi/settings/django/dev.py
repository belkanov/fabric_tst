from .base import *

from rest_framework.serializers import HyperlinkedModelSerializer

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# сюда можно добавить какие-нить модули для отладки
# INSTALLED_APPS.extend([
#     'app',
# ])


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += (
    'rest_framework.authentication.SessionAuthentication',
)

ENV_MODEL_SERIALIZER = HyperlinkedModelSerializer

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db': {
            'level': 'DEBUG'
        },
    },
}
