# isort:skip
import os
from django.core.wsgi import get_wsgi_application  # isort:skip

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()
