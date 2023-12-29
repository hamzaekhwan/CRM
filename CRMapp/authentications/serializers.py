from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from CRMapp.models import *


class UserProfileSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = UserProfile
        fields='__all__'



class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
   
    isAdmin = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin',]

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name

        return name
    
    
    
 



class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    company_name= serializers.SerializerMethodField(read_only=True)
    role=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token',"company_name","role"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
    def get_company_name(self, obj):
        user=obj.id
        profile=UserProfile.objects.get(user=user)
        company_name=profile.company_name
        return company_name
    
    def get_role(self, obj):
        user=obj.id
        profile=UserProfile.objects.get(user=user)
        if profile.isMaint:
            return 'maintenance'
        elif profile.isManager:
            return 'manager'
        elif profile.isMangerMaint:
            return 'maintenance_Manager'
        elif profile.isEmp:
            return 'employee'
        else:
            return 'No Role Assigned'
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"message": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"message": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance