# tasks/tasks.py
from django.utils import timezone
from CRMapp.models import Reminder
from django.core.mail import EmailMessage 
# from django.contrib.auth.models import User

def send_reminder_notifications():
    now = timezone.now()
    reminders_to_notify = Reminder.objects.filter(
        reminder_datetime__lte=now,
        notification_sent=False
    )

    for reminder in reminders_to_notify:
        # Perform the logic to send the notification
        # For now, we'll send an email to the admin
        admin_email = reminder.admin.email
        subject = f"Reminder Notification for {reminder.client.name}"
        message = f"Hello {reminder.admin.username},\n\n"
        message += f"This is a reminder for {reminder.client.name}: {reminder.message}\n\n"
        message += f"Reminder date and time: {reminder.reminder_datetime}\n\n"
        message += "Thank you!"
        
        email_for_send = EmailMessage(  
                        subject, message, to=[admin_email] 
            )

        email_for_send.send()  

        # Update the notification_sent field
        reminder.notification_sent = True
        reminder.save()
