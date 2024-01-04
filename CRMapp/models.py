


from django.db import models
from .validators import phone_regex
from .choises import *
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user=models.OneToOneField(User ,unique=True, on_delete=models.CASCADE)
    company_name=models.CharField("Name Of Company",choices=COMPANY_NAME, max_length=255)
    isMaint=models.BooleanField("isMaint",default=False)   #عامل صيانة IsAuthenticatedAndIsMaint
    isManager=models.BooleanField("isManager",default=False) #مدير كل شيء isAdminUser
    isMangerMaint=models.BooleanField("isMangerMaint",default=False) #مدير الصيانة isAdminUser
    isEmp=models.BooleanField("isEmp",default=False)#موظف عادي isAuth

class Client(models.Model):
    name=models.CharField("Name of Client", max_length=64)
    
    mobile_phone=models.CharField(validators=[phone_regex], max_length=17)
    arabic_name=models.CharField("Arabic Name of Client", max_length=64)
    city=models.CharField("city", max_length=64)
    # notes=models.TextField(blank=True)
    date=models.DateField("Date of client register",blank=True,null=True)
    
    def __str__(self):
        return str(self.name ) 


class Interest(models.Model):
    client=models.ForeignKey(Client,unique=False , on_delete=models.CASCADE)
    inquiry=models.BooleanField("INQUIRY",default=True)
    company_name=models.CharField("Name Of Company",choices=COMPANY_NAME, max_length=255)

    def __str__(self):
        return str(self.client.name ) + " - " + str(self.company_name) 
    
class Reminder(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    admin= models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    reminder_datetime = models.DateField()
    notification_sent = models.BooleanField(default=False)  

   
class Contract(models.Model):
    interest=models.ForeignKey(Interest,unique=False , on_delete=models.CASCADE)
    
    ats=models.CharField("ATS", max_length=64)
    floors=models.CharField("floors", max_length=64,blank=True)
    lift_type=models.CharField("Type", max_length=64,blank=True)
    location=models.URLField('Location',blank=True)
    size=models.IntegerField("Size",blank=True)
    # sales_name=models.CharField("sales_name", max_length=64,blank=True)
    signed=models.BooleanField("Signed",default=False)

    # def __str__(self):
    #     return str(self.ats ) 


class MaintenanceLift(models.Model): 
    contract = models.OneToOneField(Contract, unique=True, on_delete=models.CASCADE, related_name='maintenancelift')
    maintenance_contract_number=models.CharField("Maintenance Contract Number", max_length=64)
    maintenance_contract_start_date=models.DateField("Maintainance Contract Start")
    maintenance_contract_end_date=models.DateField("Maintainance Contract End")
    maintenance_type = models.CharField("Maintenance Type",blank=True,choices=MAINTAINCANCE_CHOICES, max_length=255)
    contract_value=models.IntegerField()
    spare_parts= models.CharField("Spare parts",choices=SPARE_PARTS, max_length=255)
    brand=models.CharField("Brand", max_length=64)
    number_of_visits_per_year=models.IntegerField()
    villa_no=models.CharField("Villa Number", max_length=64)
    handing_over_date=models.DateField("Handing Over Date")
    free_maintenance_expiry_date=models.DateField("free maintenance expiry date")


    def __str__(self):
        return str(self.maintenance_contract_number ) 


class Phase(models.Model):
    contract=models.ForeignKey(Contract,unique=False , on_delete=models.CASCADE)
    Name=models.CharField("Name of Phase",choices=PHASES_NAME, max_length=64)
    isActive=models.BooleanField(default=False)
    start_date=models.DateField("Phase Date Start")
    end_date=models.DateField("Phase Date End",blank=True,null=True)
    
    def __str__(self):
        return str(self.contract) + " " + str(self.Name ) 
   
  
class Note(models.Model)    :
    
    contract=models.ForeignKey(Contract,unique=False , on_delete=models.CASCADE)
    note=models.TextField("Notes",blank=True)
    attachment=models.FileField(blank=True)
    date=models.DateField("Date of note")
    
    def __str__(self):
        return str(self.contract) + " " + str(self.date)

   ###########################################################\

  
 

class Maintenance(models.Model):
    contract = models.ForeignKey(Contract, unique=False, on_delete=models.CASCADE)
    maintenance_lift = models.ForeignKey(MaintenanceLift, unique=False, on_delete=models.CASCADE)
    type_name = models.CharField("Type of Maintenance", choices=MAINTENANCETYPE_CHOICES, max_length=255)
    remarks = models.TextField()
    technician = models.CharField("Name Of technician", max_length=255)
    helper1 = models.CharField("Name Of helper1", max_length=255,blank=True)
    helper2 = models.CharField("Name Of helper2", max_length=255,blank=True)
    date = models.DateField("Date of remark")

    def __str__(self):
        return str(self.contract) + " " + str(self.type_name)

    
class CheckImage(models.Model):
    maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE)
    image = models.FileField()

    def __str__(self):
        return f"Image for {self.maintenance}"    
    
class PdfMaintenanceContract(models.Model):
    maintenance = models.OneToOneField(Maintenance, on_delete=models.CASCADE)
    file = models.FileField(blank=True)

    def __str__(self):
        return f"Pdf Maintenance Contract {self.maintenance}"
