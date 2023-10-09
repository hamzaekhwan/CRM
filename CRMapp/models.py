


from django.db import models

from .validators import phone_regex



class Client(models.Model):
    name=models.CharField("Name of Client", max_length=64)
    ats=models.CharField("ATS", max_length=64)
    mobile_phone=models.CharField(validators=[phone_regex], max_length=17)
    arabic_name=models.CharField("Arabic Name of Client", max_length=64)
    city=models.CharField("city", max_length=64)
    
MAINTAINCANCE_CHOICES=(
    ('FREE', 'FREE'),
    ('PAID', 'PAID'),
    )

SPARE_PARTS=(
    ('COMPREHENSIVE', 'COMPREHENSIVE'),
    ('REGULAR', 'REGULAR'),
    )

class ElevatorContract(models.Model):
    
    client=models.ForeignKey(Client,unique=False , on_delete=models.PROTECT)
    
    maintenance_contract_number=models.CharField("Maintenance Contract Number", max_length=64)
    maintenance_contract_start_date=models.DateTimeField("Maintainance Contract Start")
    maintenance_contract_end_date=models.DateTimeField("Maintainance Contract End")
   
    type_maintenance = models.CharField("maintenance Type",choices=MAINTAINCANCE_CHOICES, max_length=255)
    # @NOTE: what is contract value?
    contract_value=models.IntegerField()
    spare_parts= models.CharField("Spare parts",choices=SPARE_PARTS, max_length=255)
    # @NOTE: if the types are fixed, make it choices, if not. keep it
    type=models.CharField("Type", max_length=64)
    size=models.IntegerField("Size")
    floors=models.IntegerField("Floors")
    brand=models.CharField("Brand", max_length=64)
    number_of_visits_per_year=models.IntegerField()
    villa_no=models.IntegerField()
    # @NOTE: I think it would be best to use location as url field
    location=models.CharField("Location" ,max_length=255)
    handing_over_date=models.DateTimeField("Handing Over Date")
    free_maintenance_expiry_date=models.DateTimeField("free maintenance expiry date")
    

PHASES_NAME=(
    ('INQUIRY', 'INQUIRY'),
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
    client=models.ForeignKey(Client,unique=False , on_delete=models.PROTECT)
    contract=models.ForeignKey(ElevatorContract,unique=False , on_delete=models.PROTECT)
    Name=models.CharField("Name of Phase",choices=PHASES_NAME, max_length=64)
    isActive=models.BooleanField(default=False)
    start_date=models.DateTimeField("Phase Date Start")
    end_date=models.DateTimeField("Phase Date End",blank=True,null=True)

   

class Note(models.Model)    :
    client=models.ForeignKey(Client,unique=False , on_delete=models.PROTECT)
    contract=models.ForeignKey(ElevatorContract,unique=False , on_delete=models.PROTECT)
    note=models.TextField("Notes",blank=True)
    attachment=models.FileField(blank=True)
    date=models.DateTimeField("Date of note")