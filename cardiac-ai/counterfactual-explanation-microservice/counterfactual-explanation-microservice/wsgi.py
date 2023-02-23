import os
import consumer
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'CounterfactualExplanationMicroserivce.settings')

application = get_wsgi_application()
