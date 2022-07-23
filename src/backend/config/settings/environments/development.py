import logging
import socket
import typing

from config.settings.components.common import DATABASES
from config.settings.components.common import INSTALLED_APPS
from config.settings.components.common import MIDDLEWARE

# Setting the development status:

DEBUG = True

ALLOWED_HOSTS = [
    'foodgram',
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]

INSTALLED_APPS += (
    # Better debug:
    'debug_toolbar',
    'nplusone.ext.django',

    # Linting migrations:
    'django_migration_linter',

    # django-test-migrations:
    'django_test_migrations.contrib.django_checks.AutoNames',
    'django_test_migrations.contrib.django_checks.DatabaseConfiguration',

    # django-extra-checks:
    'extra_checks',
)

# Static files:
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-STATICFILES_DIRS

STATICFILES_DIRS: typing.List[str] = [

]

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    'querycount.middleware.QueryCountMiddleware',
)

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        '{0}.1'.format(ip[:ip.rfind('.')])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except socket.error:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ['127.0.0.1', '10.0.2.2']


def _custom_show_toolbar(request) -> bool:
    """Only show the debug toolbar to users with the superuser flag."""
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'config.settings._custom_show_toolbar',
}

MIDDLEWARE = [  # noqa: WPS440
    'nplusone.ext.django.NPlusOneMiddleware',
] + MIDDLEWARE

NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.WARN
NPLUSONE_WHITELIST = [
    {'model': 'admin.*'},
]

# django-test-migrations
# https://github.com/wemake-services/django-test-migrations

# Set of badly named migrations to ignore:
# DTM_IGNORED_MIGRATIONS = frozenset((
#     (),
# ))

# django-extra-checks
# https://github.com/kalekseev/django-extra-checks

EXTRA_CHECKS = {
    'checks': [
        # Require non empty `upload_to` argument:
        'field-file-upload-to',
        # Use the indexes option instead:
        'no-index-together',
        # FileField/ImageField must have non empty `upload_to` argument:
        'field-file-upload-to',
        # Text fields shouldn't use `null=True`:
        'field-text-null',
        # Prefer using BooleanField(null=True) instead of NullBooleanField:
        'field-boolean-null',
        # Don't pass `null=False` to model fields (this is django default)
        'field-null',
        # ForeignKey fields must specify db_index explicitly if used in
        # other indexes:
        {'id': 'field-foreign-key-db-index', 'when': 'indexes'},
        # If field nullable `(null=True)`,
        # then default=None argument is redundant and should be removed:
        'field-default-null',
        # Fields with choices must have companion CheckConstraint
        # to enforce choices on database level
        'field-choices-constraint',
    ],
}

# Disable persistent DB connections
# https://docs.djangoproject.com/en/3.2/ref/databases/#caveats

DATABASES['default']['CONN_MAX_AGE'] = 0
