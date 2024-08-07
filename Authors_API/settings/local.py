from .base import * #noqa
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY", default="0uAnLA5u0u6UX1d6PfR2npE84HfqfRYSEXb87-sc4C97Ew5bNsg",)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CSRF_TRUSTED_ORIGINS= ["http://localhost:8080"]