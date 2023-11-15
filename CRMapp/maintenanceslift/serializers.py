from rest_framework import serializers
from CRMapp.models import *

from CRMapp.contracts.serializers import ContractSerializer

class MaintenanceLiftSerializer(serializers.ModelSerializer):
    contract=serializers.SerializerMethodField()
    class Meta:
        model = MaintenanceLift
        fields = [
                
                'id',
                'contract',
                'maintenance_contract_number',
                'maintenance_contract_start_date',
                'maintenance_contract_end_date',
                'maintenance_type',
                'contract_value',
                'spare_parts',
                'brand',
                'number_of_visits_per_year',
                'villa_no',
                'handing_over_date',
                'free_maintenance_expiry_date',
                  
        ]
    
    def get_contract(self, obj):
        query=Contract.objects.get(id=obj.contract.id)
        serializer=ContractSerializer(query,many=False)
        return serializer.data


   
