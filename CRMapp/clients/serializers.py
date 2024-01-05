from rest_framework import serializers
from CRMapp.models import *
from CRMapp.authentications.serializers import UserSerializer

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
    client=serializers.SerializerMethodField()
    admin= serializers.SerializerMethodField()
    class Meta:
        model = Reminder
        fields = [
                
                'id',
                'client',
                'admin',
                'message',
                'reminder_datetime',
                'notification_sent',
               
               
                  
        ]

    def get_client(self, obj):
        query=Client.objects.get(id=obj.client.id)
        serializer=InterClientSerializer(query,many=False)
        return serializer.data    
    
    def get_admin(self, obj):
        query=User.objects.get(id=obj.admin.id)
        serializer=UserSerializer(query,many=False)
        return serializer.data  
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
                'date',
                'interest',
                'reminder',
                'notes',
                  
        ]
    def get_interest(self, obj):
        query=Interest.objects.filter(client=obj.id)
        serializer=InterestSerializer(query,many=True)
        return serializer.data
    
    def get_reminder(self, obj):
        query=Reminder.objects.filter(client=obj.id)
        serializer=ReminderSerializer(query,many=True)
        return serializer.data

class DistinctCitySerializer(serializers.Serializer):
    city = serializers.CharField()

