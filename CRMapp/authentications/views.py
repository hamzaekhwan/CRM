from django.shortcuts import render
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from django.shortcuts import get_object_or_404
from .permissions import * 
from django.contrib.auth.hashers import make_password
# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)

        
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer     


class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            data=request.data
            old_password=data['old_password']
            password=data['password']
            password2=data['password2']
            # serializer = self.get_serializer(data=request.data)
            
            
          
                # Check old password
               
            if not self.object.check_password(old_password):
                return Response({"message": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(password)
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)
        

@api_view(['POST','PUT','GET','DELETE'])
@permission_classes([IsManager])
def admin(request,pk=None):
    if request.method=="POST":
        
        data=request.data
        username=data['username']
        email=data.get('email', "")
        password=data['password']
        
        name=data['name']
        company_name=data['company_name']
        isMaint=data['isMaint']
        isManager=data['isManager']
        isMangerMaint=data['isMangerMaint']
        isEmp=data['isEmp']

        user_exists = User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()
        if not user_exists:
            user = User.objects.create_user(username=username, email=email, password=make_password(password))
            user.save()

            profile = UserProfile.objects.create(
                user=user,
                company_name=company_name,
                isMaint=isMaint,
                isManager=isManager,
                isMangerMaint=isMangerMaint,
                isEmp=isEmp
            )
            user.first_name=name
            if profile.isEmp== "True" or profile.isManager=="True" or profile.isMangerMaint=="True" : 
                user.is_superuser=True
                user.is_staff=True 
            user.save()

            message = {'detail': 'User added successfully'}
            return Response(message)
        else :
            message = {'detail': 'User with this email or username already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "GET":
        if pk is not None:
          
            user = get_object_or_404(User, id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
          
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        
    if request.method=="DELETE":  
        user_obj = get_object_or_404(User, id=pk)
        user_obj.delete()
        message = {'detail': 'Admin deleted successfully'}
        return Response(message)
    
    if request.method=="PUT":  
        
        user_obj = get_object_or_404(User, id=pk)
        data = request.data

        # email = data.get('email', user_obj.email)
        # username = data.get('username', user_obj.username)
        name = data.get('name', user_obj.first_name)

        # user_obj.email = email
        # user_obj.username = username
        user_obj.first_name = name

        profile=UserProfile.objects.get(user=user_obj)

        company_name = data.get('company_name', profile.company_name)
        isMaint = data.get('isMaint', profile.isMaint)
        isManager = data.get('isManager', profile.isManager)
        isMangerMaint = data.get('isMangerMaint', profile.isMangerMaint)
        isEmp = data.get('isEmp', profile.isEmp)

        profile.company_name=company_name
        profile.isMaint=isMaint
        profile.isManager=isManager
        profile.isMangerMaint=isMangerMaint
        profile.isEmp=isEmp

        profile.save()

        if profile.isEmp=="True" or profile.isManager=="True" or profile.isMangerMaint=="True" : 
            user_obj.is_superuser=True
            user_obj.is_staff=True

        if profile.isMaint == "True" : 
            user_obj.is_superuser=False
            user_obj.is_staff=False
       
        user_obj.save()

        message = {'detail': 'User updated successfully'}
        return Response(message)



