import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
app = Celery("ctest")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(5.0, add_noti_beat.s(), name='add every 10')


app.conf.beat_schedule = {
    "send_notifications": {
        "task": "mysite.celery.noti_beat",
        "schedule": 10.0,  # every n seconds
    },
    # "send_notifications2": {
    #     "task": "mysite.celery.noti_delay",
    #     "schedule": 2.0,  # every n seconds
    # },
}
from functools import wraps
def skip_if_running(f):
    task_name = f'{f.__module__}.{f.__name__}'

    @wraps(f)
    def wrapped(self, *args, **kwargs):
        workers = self.app.control.inspect().active()
        for worker, tasks in workers.items():
            for task in tasks:
                if (task_name == task['name'] and
                        tuple(args) == tuple(task['args']) and
                        kwargs == task['kwargs'] and
                        self.request.id != task['id']):
                    print(f'task {task_name} ({args}, {kwargs}) is running on {worker}, skipping')
                    return None
        return f(self, *args, **kwargs)
    return wrapped


def send_webhook(m="hai"):
    from json import dumps
    import requests
    from datetime import datetime

    requests.post(
        "https://chat.googleapis.com/v1/spaces/AAAAlng2ZTM/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=LooiI2-CA-IFjSC_q47X-zaVgB2l4ivSnAc05H1W6ug",
        headers={"Content-Type": "application/json"},
        data=dumps({"text": f"{datetime.now()}: {m}"}),
    )

@skip_if_running
@app.task(queue="high_priority")
def noti_delay():
    import time
    time.sleep(5)

    # from sampleapp.models import Notification
    # Notification.objects.create(title='celery')
    send_webhook("notification delay")

# @skip_if_running
@app.task
def noti_beat():
    from sampleapp.models import Notification
    Notification.objects.create(title='notification')
    send_webhook("notification beat")


