from rest_framework import serializers
from CRMapp.models import *





class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields='__all__'


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields='__all__'


class ElevatorContractSerializer(serializers.ModelSerializer):
    notes=serializers.SerializerMethodField()
    current_phase=serializers.SerializerMethodField()
    client=serializers.SerializerMethodField()
    class Meta:
        model = ElevatorContract
        fields = [
                
                'id',
                'client',
                'maintenance_contract_number',
                'maintenance_contract_start_date',
                'maintenance_contract_end_date',
                'type_maintenance',
                'contract_value',
                'spare_parts',
                'type',
                'size',
                'floors',
                'brand',
                'number_of_visits_per_year',
                'villa_no',
                'location',
                'handing_over_date',
                'free_maintenance_expiry_date',
                'notes',
                'current_phase',
                  
        ]
    
    def get_client(self, obj):
        return obj.client.name

    def get_notes(self, obj):
        
        contract=ElevatorContract.objects.filter(id=obj.id).first()
        
        
        query=Note.objects.filter(client=obj.client,contract=contract)
        serializer=NoteSerializer(query,many=True)
        return serializer.data
    
    def get_current_phase(self, obj):
        contract=ElevatorContract.objects.get(id=obj.id)
        current_phase=Phase.objects.filter(client=obj.client,contract=contract,isActive=True).first()
        serializer=PhaseSerializer(current_phase,many=False)
        return serializer.data
            





