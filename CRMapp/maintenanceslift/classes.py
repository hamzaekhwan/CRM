from django.contrib import admin
from CRMapp.models import *



from CRMapp.functions import *





class MaintenanceLiftAdmin(admin.ModelAdmin):
    list_display = ['contract', 'brand', 'maintenance_type', 'number_of_visits_per_year']
    list_filter = ['spare_parts','number_of_visits_per_year']
    search_fields=['maintenance_contract_number','villa_no','contract__ats']
    actions = [export_to_excel,export_to_pdf,export_to_csv] 