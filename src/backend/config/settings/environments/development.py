import socket
import typing

from config.settings.components import config
from config.settings.components.common import DATABASES
from config.settings.components.common import INSTALLED_APPS
from config.settings.components.common import MIDDLEWARE

# Setting the development status:

# GENERAL
# ------------------------------------------------------------------------------

DEBUG = True

SECRET_KEY = config('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    config('DOMAIN_NAME'),
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]

# THIRD PARTY APPS
# ------------------------------------------------------------------------------

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

# STATIC:
# ------------------------------------------------------------------------------

STATIC_URL = config('DJANGO_STATIC_URL', default='/static/')
STATIC_ROOT = '/var/www/django/static'

STATICFILES_DIRS: typing.List[str] = [

]

# MEDIA
# ------------------------------------------------------------------------------

MEDIA_URL = config('DJANGO_MEDIA_URL', default='/media/')
MEDIA_ROOT = '/var/www/django/media'


# DEBUG-TOOLBAR
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    'querycount.middleware.QueryCountMiddleware',
)

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
    # raise ValueError(request.user.is_superuser)
    return DEBUG and request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': ['debug_toolbar.panels.redirects.RedirectsPanel'],
    'SHOW_TEMPLATE_CONTEXT': True,
    'SHOW_TOOLBAR_CALLBACK': 'config.settings._custom_show_toolbar',
}

# NPlusOne
# ------------------------------------------------------------------------------
# https://github.com/jmcarp/nplusone

# MIDDLEWARE = [  # noqa: WPS440
#     'nplusone.ext.django.NPlusOneMiddleware',
# ] + MIDDLEWARE
#
# NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
# NPLUSONE_LOGGER = logging.getLogger('nplusone')
# NPLUSONE_LOG_LEVEL = logging.WARN
# NPLUSONE_WHITELIST = [
#     {'model': 'admin.*'},
# ]

# DJANGO-TEST-MIGRATIONS
# ------------------------------------------------------------------------------
# https://github.com/wemake-services/django-test-migrations

# Set of badly named migrations to ignore:
DTM_IGNORED_MIGRATIONS = frozenset((
    ('authtoken', '*'),
))

# DJANGO-EXTRA-CHECKS
# ------------------------------------------------------------------------------
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

# DATABASES
# Disable persistent DB connections
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/databases/#caveats

DATABASES['default']['CONN_MAX_AGE'] = 0
