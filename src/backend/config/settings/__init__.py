"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
To change settings file:
`DJANGO_ENV=production`
"""

import django_stubs_ext
from environs import Env
from split_settings.tools import include
from split_settings.tools import optional

env = Env()

# Monkeypatching Django, so stubs will work for all generics,
# see: https://github.com/typeddjango/django-stubs
django_stubs_ext.monkeypatch()

# Managing environment via `DJANGO_ENV` variable:
_ENV = env('DJANGO_ENV', 'development')

_base_settings = (
    'components/common.py',
    'components/logging.py',

    # Select the right env:
    'environments/{0}.py'.format(_ENV),

    # Optionally override some settings:
    optional('environments/local.py'),
)

# Include settings:
include(*_base_settings)
