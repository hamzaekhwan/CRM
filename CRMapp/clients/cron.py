# في ملف CRMapp/cron.py

from django_cron import CronJobBase, Schedule
from django.utils import timezone
from CRMapp.models import Reminder

class DailyReminderJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # يعمل كل دقيقة واحدة (يوميًا)

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'CRMapp.clients.cron.DailyReminderJob'

    def do(self):
        # القضاء على التذكيرات التي لم يتم إرسال إشعار لها بعد والتي يجب إرسالها اليوم
        reminders_to_send = Reminder.objects.filter(
            reminder_datetime__date=timezone.now().date(),
            notification_sent=False
        )

        for reminder in reminders_to_send:
            # يمكنك هنا إضافة الكود الخاص بإرسال الإشعار
            # ثم قم بتحديث حالة notification_sent إلى True
            reminder.notification_sent = True
            reminder.save()
