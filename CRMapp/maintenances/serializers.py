from rest_framework import serializers
from CRMapp.models import *





class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields='__all__'
