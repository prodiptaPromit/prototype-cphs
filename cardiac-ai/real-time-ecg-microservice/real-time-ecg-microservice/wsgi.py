import os
import consumer
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealTimeEcgSerivce.settings')

application = get_wsgi_application()
