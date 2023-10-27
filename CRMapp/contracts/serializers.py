from rest_framework import serializers
from CRMapp.models import *
from CRMapp.clients.serializers import InterestSerializer





class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields='__all__'


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields='__all__'


class ContractSerializer(serializers.ModelSerializer):
    notes=serializers.SerializerMethodField()
    current_phase=serializers.SerializerMethodField()
    interest=serializers.SerializerMethodField()
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
                  
        ]
    
    def get_interest(self, obj):
        query=Interest.objects.get(id=obj.interest.id)
        serializer=InterestSerializer(query,many=False)
        return serializer.data

    def get_notes(self, obj):
        
        contract=Contract.objects.filter(id=obj.interest.client.id).first()
        
        
        query=Note.objects.filter(contract=contract)
        serializer=NoteSerializer(query,many=True)
        return serializer.data
    
    def get_current_phase(self, obj):
        contract=Contract.objects.filter(id=obj.interest.client.id).first()
        current_phase=Phase.objects.filter(contract=contract,isActive=True)
        return current_phase.first().Name





