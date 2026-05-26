web: gunicorn myapp.wsgi:application
worker: celery -A myapp worker -l info
beat: celery -A myapp beat -l info
