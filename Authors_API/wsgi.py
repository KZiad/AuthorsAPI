"""
WSGI config for Authors_API project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
    #TODO: change to production

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Authors_API.settings.local")

application = get_wsgi_application()
