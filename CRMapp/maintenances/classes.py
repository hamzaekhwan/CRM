from django.contrib import admin
from CRMapp.models import *
from CRMapp.functions import *

class MaintenanceInline(admin.TabularInline):
    model = Maintenance
    extra = 1

class MaintenanceAdmin(admin.ModelAdmin):
    list_filter= ['type_name']
    list_display = ['client','contract','type_name','date']
    search_fields=['client','contract',]    
    actions = [export_to_excel,export_to_pdf,export_to_csv] 