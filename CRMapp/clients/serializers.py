from rest_framework import serializers
from CRMapp.models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields='__all__'