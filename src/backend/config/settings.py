import socket
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('DJANGO_SECRET_KEY', 'SET DJANGO_SECRET_KEY')

DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['127.0.0.1', 'localhost'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',

    'apps.users',
    'apps.tags',
    'apps.ingredients',
    'apps.recipes',
    'apps.favourites',
    'apps.subscriptions',
    'apps.carts',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': env.dj_db_url('DATABASE_URL', 'postgres://...'),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = env.str('DJANGO_STATIC_URL', '/static/')
STATIC_ROOT = '/static'

MEDIA_URL = env.str('DJANGO_MEDIA_URL', '/media/')
MEDIA_ROOT = '/media'

AUTH_USER_MODEL = 'users.CustomUser'

if DEBUG:
    # https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
    try:  # This might fail on some OS
        INTERNAL_IPS = [
            '{0}.1'.format(ip[:ip.rfind('.')])
            for ip in socket.gethostbyname_ex(socket.gethostname())[2]
        ]
    except socket.error:  # pragma: no cover
        INTERNAL_IPS = []
    INTERNAL_IPS += ['127.0.0.1', '10.0.2.2']


def _custom_show_toolbar(request):
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'config.settings._custom_show_toolbar',
}
