from rest_framework import serializers
from CRMapp.models import *
from CRMapp.clients.serializers import ClientSerializer





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
    client=serializers.SerializerMethodField()
    class Meta:
        model = Contract
        fields = [
                
                'id',
                'ats',
                'client',
                'lift_type',
                'size',
                'floors',
                'location',
                'notes',
                'current_phase',
                  
        ]
    
    def get_client(self, obj):
        query=Client.objects.get(id=obj.client.id)
        serializer=ClientSerializer(query,many=False)
        return serializer.data

    def get_notes(self, obj):
        
        contract=Contract.objects.filter(id=obj.id).first()
        
        
        query=Note.objects.filter(client=obj.client,contract=contract)
        serializer=NoteSerializer(query,many=True)
        return serializer.data
    
    def get_current_phase(self, obj):
        contract=Contract.objects.get(id=obj.id)
        current_phase=Phase.objects.filter(client=obj.client,contract=contract,isActive=True).first()
        serializer=PhaseSerializer(current_phase,many=False)
        return serializer.data
            





