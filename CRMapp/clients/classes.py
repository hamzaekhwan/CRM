from django.contrib import admin
from CRMapp.models import *
from CRMapp.contracts.classes import ContractInline,PhaseInline


from CRMapp.functions import *





class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'mobile_phone', 'arabic_name', 'city']
    list_filter = ['city']
    search_fields=['mobile_phone','arabic_name','name']
    actions = [export_to_excel,export_to_pdf,export_to_csv] 
    # inlines = [ContractInline,PhaseInline]