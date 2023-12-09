from rest_framework import serializers
from CRMapp.models import *





# class MaintenanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Maintenance
#         fields='__all__'
# from rest_framework import serializers

class CheckImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckImage
        fields = ('id', 'image')

class PdfMaintenanceContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = PdfMaintenanceContract
        fields = ('id', 'file')        

class MaintenanceSerializer(serializers.ModelSerializer):
    check_images = serializers.SerializerMethodField(read_only=True)
    pdf_maintenance_contract = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Maintenance
        fields =('contract', 'maintenance_lift','type_name','remarks','technician','helper1','helper1','date','check_images','pdf_maintenance_contract')

    def get_check_images(self, obj):
        images=CheckImage.objects.filter(maintenance=obj.id)
        serializer=CheckImageSerializer(images,many=True)
        return serializer.data
    
    def get_pdf_maintenance_contract(self, obj):
        files=PdfMaintenanceContract.objects.filter(maintenance=obj.id)
        serializer=PdfMaintenanceContractSerializer(files,many=True)
        return serializer.data