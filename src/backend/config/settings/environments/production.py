from config.settings.components import env
from config.settings.components.common import INSTALLED_APPS

# Setting the production status:

DEBUG = False

SECRET_KEY = env.str('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'foodgram',
]

INSTALLED_APPS += (
    # AWS storage:
    'storages',
)

# STORAGES
# ------------------------------------------------------------------------------

AWS_S3_ENDPOINT_URL = env.str('AWS_S3_ENDPOINT_URL')
AWS_ACCESS_KEY_ID = env.str('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env.str('DJANGO_AWS_STORAGE_BUCKET_NAME')
_AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
}
AWS_LOCATION = 'static'

# STATIC
# ------------------------------------------------------------------------------

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
COLLECTFAST_STRATEGY = 'collectfast.strategies.boto3.Boto3Strategy'

SPA_MANIFEST_FILEPATH = env.str('SPA_MANIFEST_FILEPATH')
SPA_BASE_URL = env.str('SPA_BASE_URL')
