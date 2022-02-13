import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
#BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')

app = Celery('mysite') #might need changing

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

# this allows you to schedule items in the Django admin.
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'

# may need to adjust later, need to confirm if schedule is on pst
# and additionally NYSE opens at 9:30 AM - 4 PM 
app.conf.beat_schedule = {
    'scrape_movers_on_weekdays': {
        'task': 'scrape_mover_info',
        'schedule': crontab(day_of_week='mon-fri', hour='5-14', minute=0)
    },
    'scrape_articles_on_weekdays': {
        'task': 'scrape_articles_for_selected_stock',
        'schedule': crontab(day_of_week='mon-fri', hour='7,16', minute=15)
    },
}