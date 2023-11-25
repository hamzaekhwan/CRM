# في ملف CRMapp/apps.py

from django.apps import AppConfig
# from django_cron import CronJobBase, Schedule


class CrmappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CRMapp'

    def ready(self):
        print("start Schedule .... ")
        import CRMapp.signals
        from CRMapp.clients import updater
        updater.start()
       
        
