from rest_framework import serializers
from CRMapp.models import *


class InterClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields='__all__'

class InterestSerializer(serializers.ModelSerializer):  
    client=serializers.SerializerMethodField()
    class Meta:
        model = Interest
        fields = [
                'id',
                'client',
                'company_name']
        
    def get_client(self, obj):
        query=Client.objects.get(id=obj.client.id)    
        serializer=InterClientSerializer(query,many=False)
        return serializer.data

class ReminderSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Reminder
        fields='__all__'

class ClientSerializer(serializers.ModelSerializer):
    interest=serializers.SerializerMethodField()
    reminder=serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = [
                
                'id',
                'name',
                'mobile_phone',
                'arabic_name',
                'city',
                'inquiry',
                'date',
                'interest',
                'reminder',
                  
        ]
    def get_interest(self, obj):
        query=Interest.objects.filter(client=obj.id)
        serializer=InterestSerializer(query,many=True)
        return serializer.data
    
    def get_reminder(self, obj):
        query=Reminder.objects.filter(client=obj.id)
        serializer=ReminderSerializer(query,many=True)
        return serializer.data



