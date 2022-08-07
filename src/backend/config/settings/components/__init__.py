from os import environ
from pathlib import Path

from decouple import AutoConfig

BASE_DIR = Path(__file__).parent.parent.parent.parent

# Managing environment via `DJANGO_ENV` variable:
environ.setdefault('DJANGO_ENV', 'development')
_ENV = environ['DJANGO_ENV']

config = AutoConfig(
    search_path=BASE_DIR.joinpath(f'.envs/{_ENV}'),
)
