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

class MaintenanceSerializer(serializers.ModelSerializer):
    check_images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Maintenance
        fields =('contract', 'maintenance_lift','type_name','remarks','technician','helper1','helper1','date','check_images')

    def get_check_images(self, obj):
        images=CheckImage.objects.filter(maintenance=obj.id)
        serializer=CheckImageSerializer(images,many=True)
        return serializer.data