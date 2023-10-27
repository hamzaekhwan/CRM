


from django.db import models
from .validators import phone_regex
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Client(models.Model):
    name=models.CharField("Name of Client", max_length=64)
    
    mobile_phone=models.CharField(validators=[phone_regex], max_length=17)
    arabic_name=models.CharField("Arabic Name of Client", max_length=64)
    city=models.CharField("city", max_length=64)
    inquiry=models.BooleanField("INQUIRY",default=True)
    date=models.DateTimeField("Date of client register",blank=True,null=True)
    
    def __str__(self):
        return str(self.name ) 


COMPANY_NAME=(
    ('ATLAS', 'ATLAS'),
    ('KEILANI_INTERIORS', 'KEILANI_INTERIORS'),
    ('NAMMOUS', 'NAMMOUS'),
    ('KCC', 'KCC'),
    ('SMART', 'SMART'),
    ('AC', 'AC'),
    ('LAND_SCAPE', 'LAND_SCAPE'),
    ('SWIMMING_POOL', 'SWIMMING_POOL'),
    )
class Interest(models.Model):
    client=models.ForeignKey(Client,unique=False , on_delete=models.PROTECT)
    company_name=models.CharField("Name Of Company",choices=COMPANY_NAME, max_length=255)


class Reminder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    reminder_datetime = models.DateTimeField()
    notification_sent = models.BooleanField(default=False)  

    
class Contract(models.Model):
    interest=models.ForeignKey(Interest,unique=False , on_delete=models.PROTECT)
    
    ats=models.CharField("ATS", max_length=64)
    floors=models.CharField("floors", max_length=64)
    lift_type=models.CharField("Type", max_length=64)
    location=models.URLField('Location')
    size=models.IntegerField("Size")

    def __str__(self):
        return str(self.ats ) 
MAINTAINCANCE_CHOICES=(
    ('FREE', 'FREE'),
    ('PAID', 'PAID'),
    )
SPARE_PARTS=(
    ('COMPREHENSIVE', 'COMPREHENSIVE'),
    ('REGULAR', 'REGULAR'),
    )
class MaintenanceLift(models.Model): 
    contract=models.ForeignKey(Contract,unique=False , on_delete=models.PROTECT)
    maintenance_contract_number=models.CharField("Maintenance Contract Number", max_length=64)
    maintenance_contract_start_date=models.DateTimeField("Maintainance Contract Start")
    maintenance_contract_end_date=models.DateTimeField("Maintainance Contract End")
    maintenance_type = models.CharField("Maintenance Type",blank=True,choices=MAINTAINCANCE_CHOICES, max_length=255)
    contract_value=models.IntegerField()
    spare_parts= models.CharField("Spare parts",choices=SPARE_PARTS, max_length=255)
    brand=models.CharField("Brand", max_length=64)
    number_of_visits_per_year=models.IntegerField()
    villa_no=models.CharField("Villa Number", max_length=64)
    handing_over_date=models.DateTimeField("Handing Over Date")
    free_maintenance_expiry_date=models.DateTimeField("free maintenance expiry date")


    def __str__(self):
        return str(self.maintenance_contract_number ) 

PHASES_NAME=(
    
    ('SALES', 'SALES'),
    ('ENG', 'ENG'),
    ('SIGNED_CONTRACT', 'SIGNED_CONTRACT'),
    ('MANUFACTURING', 'MANUFACTURING'),
    ('DELIVERY', 'DELIVERY'),
    ('INSTALLATION', 'INSTALLATION'),
    ('MECHANICAL', 'MECHANICAL'),
    ('ELECTRICAL', 'ELECTRICAL'),
    ('HANDING_OVER', 'HANDING_OVER'),
    ('MAINTENANCE', 'MAINTENANCE'),
    )

class Phase(models.Model):
    contract=models.ForeignKey(Contract,unique=False , on_delete=models.PROTECT)
    Name=models.CharField("Name of Phase",choices=PHASES_NAME, max_length=64)
    isActive=models.BooleanField(default=False)
    start_date=models.DateTimeField("Phase Date Start")
    end_date=models.DateTimeField("Phase Date End",blank=True,null=True)
    
    def __str__(self):
        return str(self.contract) + " " + str(self.Name ) 
   
  
class Note(models.Model)    :
    
    contract=models.ForeignKey(Contract,unique=False , on_delete=models.PROTECT)
    note=models.TextField("Notes",blank=True)
    attachment=models.FileField(blank=True)
    date=models.DateTimeField("Date of note")
    
    def __str__(self):
        return str(self.contract) + " " + str(self.date)

   ###########################################################\

MAINTENANCETYPE_CHOICES=(
    ('EMERGENCY', 'EMERGENCY'),
    ('PREDICTIVE PERIODIC', 'PREDICTIVE PERIODIC'),
    )   
class Maintenance(models.Model):
    contract=models.ForeignKey(Contract,unique=False , on_delete=models.PROTECT)
    type_name= models.CharField("Type of Maintenance ",choices=MAINTENANCETYPE_CHOICES, max_length=255)
    remarks=models.TextField()
    signature_of_client=models.FileField(blank=True)
    signature_of_supervisor=models.FileField(blank=True)
    signature_of_technician=models.FileField(blank=True)
    date=models.DateTimeField("Date of remark")
    ###MachineRoomMaintenance
    hoist_ropes=models.BooleanField(default=True)
    coupling=models.BooleanField(default=True)
    points_of_lubrication=models.BooleanField(default=True)
    control_board=models.BooleanField(default=True)
    fuses=models.BooleanField(default=True)
    motor_protection=models.BooleanField(default=True)
    ###TractionRoomMaintenance
    governor_rope=models.BooleanField(default=True)
    is_break=models.BooleanField(default=True)
    gear_bearing=models.BooleanField(default=True)
    ###HaudraulicRoomMaintenance
    piston_units=models.BooleanField(default=True)
    oil_change=models.BooleanField(default=True)
    pumb=models.BooleanField(default=True)
    valve=models.BooleanField(default=True)
    ###PitMaintenance
    cleanliness=models.BooleanField(default=True)
    buffers=models.BooleanField(default=True)
    limit_switch=models.BooleanField(default=True)
    safety_link=models.BooleanField(default=True)
    under_drive=models.BooleanField(default=True)
    points_of_lubrication=models.BooleanField(default=True)
    ### RunTheLiftMaintenance
    landing_calls_signals=models.BooleanField(default=True)
    door_outside_hangers=models.BooleanField(default=True)
    door_close_photocell=models.BooleanField(default=True)
    leveling=models.BooleanField(default=True)
    c_o_p_lights=models.BooleanField(default=True)
    condition_of_car=models.BooleanField(default=True)    
    smooth_and_soundless_run=models.BooleanField(default=True)    
    start_stop_process=models.BooleanField(default=True)    
    door_switch_looking_device=models.BooleanField(default=True)
    ###ShaftAndCarMaintenance
    clean_lines=models.BooleanField(default=True)
    final_limits=models.BooleanField(default=True)
    car_switch=models.BooleanField(default=True)
    car_insulation=models.BooleanField(default=True)
    safety_device_link_age=models.BooleanField(default=True)
    operation_of_safet_device=models.BooleanField(default=True)    
    door_operation=models.BooleanField(default=True)    
    door_locks=models.BooleanField(default=True)    
    door_inside=models.BooleanField(default=True)
    shaft_switches=models.BooleanField(default=True)
    guide_rails_car=models.BooleanField(default=True)
    guide_rails_shoes_car=models.BooleanField(default=True)
    door_inside=models.BooleanField(default=True)
    traveling_cable=models.BooleanField(default=True)

    def __str__(self):
        return str(self.contract) + " " + str(self.type_name ) 
    