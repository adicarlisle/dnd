import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # Ensure this matches your settings folder name!

application = get_wsgi_application()

# ⚡ Vercel serverless functions require this mapping declaration:
app = application