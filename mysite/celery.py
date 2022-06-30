import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('ctest')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # from NotificationApp.tasks import add_notification
    sender.add_periodic_task(10.0, add_notification.s(), name='add every 10')


# app.conf.beat_schedule = {
#     'send_notifications': {
#         'task': 'NotificationApp.tasks.add_notification',
#         'schedule': 10.0 # every n seconds
#     }
# }


@app.task
def add_notification():
    from sampleapp.models import Notification
    Notification.objects.create(title='celery')