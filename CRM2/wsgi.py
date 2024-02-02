"""
WSGI config for CRM2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM2.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root="CRM2/staticfiles")
application.add_files("CRM2/staticfiles", prefix="CRM2/static")

