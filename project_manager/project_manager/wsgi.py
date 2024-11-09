"""
WSGI config for project_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys, pathlib
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')

path = str(pathlib.Path(__file__).parent.parent.absolute())
if path not in sys.path:
	sys.path.append(path)
	
application = get_wsgi_application()
