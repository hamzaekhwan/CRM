from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

def print_hello():
    print("Hello from the scheduled task!")

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", minutes=1)
def scheduled_job():
    print_hello()

register_events(scheduler)
scheduler.start()