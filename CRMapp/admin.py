from django.contrib import admin
from .models import *
from CRMapp.contracts.classes import ContractAdmin ,PhaseAdmin , NoteAdmin
from CRMapp.clients.classes import ClientAdmin
from CRMapp.maintenances.classes import MaintenanceAdmin




# Register your models here.
admin.site.register(Client,ClientAdmin)
admin.site.register(Contract,ContractAdmin)
admin.site.register(Note,NoteAdmin)
admin.site.register(Phase,PhaseAdmin)
admin.site.register(MaintenanceLift)
admin.site.register(Reminder)
admin.site.register(Interest)
# admin.site.register(Maintenance,MaintenanceAdmin)
