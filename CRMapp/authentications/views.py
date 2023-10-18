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
@permission_classes([IsAdminUser])
def admin(request,pk=None):
    if request.method=="POST":
        
        data=request.data
        username=data['username']
        email=data['email']
        password=data['password']
        name=data['name']
     

        superuser_exists = User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or User.objects.filter(first_name=name).exists()
        if not superuser_exists:
            superuser = User.objects.create_superuser(username, email, password)
            
    
            superuser.first_name=name
         
            superuser.save()
            message = {'detail': 'Admin added successfully'}
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

        email = data.get('email', user_obj.email)
        username = data.get('username', user_obj.username)
        name = data.get('name', user_obj.first_name)
        

        user_obj.email = email
        user_obj.username = username
        user_obj.first_name = name
       

        user_obj.save()

        message = {'detail': 'User updated successfully'}
        return Response(message)



