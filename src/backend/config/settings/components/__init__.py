from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR.parent.parent / '.env'))
