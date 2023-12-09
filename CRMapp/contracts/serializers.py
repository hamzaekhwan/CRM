from rest_framework import serializers
from CRMapp.models import *
from CRMapp.clients.serializers import InterestSerializer
# from CRMapp. .serializers import InterestSerializer
# from CRMapp.maintenanceslift.serializers import MaintenanceLiftSerializer



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields='__all__'


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields='__all__'

class ContractMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceLift
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    notes=serializers.SerializerMethodField()
    current_phase=serializers.SerializerMethodField()
    interest=serializers.SerializerMethodField()
    villa_no=serializers.SerializerMethodField()
    class Meta:
        model = Contract
        fields = [
                
                'id',
                'ats',
                'interest',
                'lift_type',
                'size',
                'floors',
                'location',
                'notes',
                'current_phase',
                'villa_no',
                  
        ]
    
    def get_interest(self, obj):
        query=Interest.objects.get(id=obj.interest.id)
        serializer=InterestSerializer(query,many=False)
        return serializer.data

    def get_notes(self, obj):
        
        contract=Contract.objects.get(id=obj.id)
        
        
        query=Note.objects.filter(contract=contract)
        serializer=NoteSerializer(query,many=True)
        return serializer.data
    
    def get_current_phase(self, obj):
        contract=Contract.objects.get(id=obj.id)
        current_phase=Phase.objects.filter(contract=contract,isActive=True)
        if current_phase.exists() :
            serializer=PhaseSerializer(current_phase , many=True)
            return serializer.data
        else: 
            a=[]
            return a
    
    
    def get_villa_no(self, obj):
        contract=Contract.objects.get(id=obj.id)
        query=MaintenanceLift.objects.filter(contract=contract)
        if query.exists() : 

            villa_no=query[0].villa_no
            return villa_no
        else : 
            return ""




