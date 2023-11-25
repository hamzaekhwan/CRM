# tasks/tasks.py
from django.utils import timezone
from CRMapp.models import Reminder
# from django.contrib.auth.models import User

def send_reminder_notifications():
    now = timezone.now()
    reminders_to_notify = Reminder.objects.filter(
        reminder_datetime__lte=now,
        notification_sent=False
    )

    for reminder in reminders_to_notify:
        # Perform the logic to send the notification
        # You might use a notification library, send an email, etc.
        # For now, we'll just print a message
        print(f"Sending reminder notification to {reminder.client.name}: {reminder.message}")

        # Update the notification_sent field
        reminder.notification_sent = True
        reminder.save()
