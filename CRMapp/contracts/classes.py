from django.contrib import admin
from CRMapp.models import *
from CRMapp.maintenances.classes import MaintenanceInline
from CRMapp.functions import *

class PhaseInline(admin.TabularInline):
    model = Phase
    extra = 1

class NoteInline(admin.TabularInline):
    model = Note
    extra = 1
    
class MaintenanceLiftInline(admin.TabularInline):
    model = MaintenanceLift
    extra = 1

class MaintenanceInline(admin.TabularInline):
    model = Maintenance
    extra = 1

class ContractInline(admin.TabularInline):
    model = Contract
    extra = 1
    list_filter = ('type_maintenance', 'spare_parts', 'type', 'brand')
    
class ContractAdmin(admin.ModelAdmin):
    list_display = ['id',]
    list_filter= ['floors']
  
    actions = [export_all_data_to_excel,export_to_excel,export_to_pdf,export_to_csv] 
    inlines = [ PhaseInline, NoteInline,MaintenanceLiftInline,MaintenanceInline]

class PhaseAdmin(admin.ModelAdmin):
    list_filter= ['Name','isActive',]
    list_display = ['contract','Name','isActive',]
    actions = [export_to_excel,export_to_pdf,export_to_csv] 
    search_fields=['contract']

class NoteAdmin(admin.ModelAdmin):
    actions = [export_to_excel,export_to_pdf,export_to_csv] 
    list_display = ['contract']
    search_fields=['contract']

