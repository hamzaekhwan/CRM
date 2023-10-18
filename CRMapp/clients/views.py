
from .serializers import *

from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from django.http import JsonResponse
from CRMapp.models import *
from django.shortcuts import get_object_or_404
@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsAdminUser])
def client(request,pk=None):
    if request.method == 'POST' :
        data=request.data

        name=data['name']
        
        client_exists = Client.objects.filter(name=name).exists() 
        if not client_exists:
            
            mobile_phone=data['mobile_phone']
            arabic_name=data['arabic_name']
            city=data['city']

            Client.objects.create(name=name,
                             
                                mobile_phone=mobile_phone,
                                arabic_name=arabic_name,
                                city=city)

            message = {'detail': 'Client added successfully'}
            return Response(message) 
        else:
            message = {'detail': 'client with this name or ATS already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    
    if request.method == 'GET' :
        if pk is not None:
            user = get_object_or_404(Client, id=pk)
            serializer = ClientSerializer(user)
            return Response(serializer.data)
        else:
            query=Client.objects.all()
            serializer=ClientSerializer(query,many=True)
            return JsonResponse(serializer.data,safe=False)
    
    if request.method == 'DELETE' :
        client=get_object_or_404(Client, id=pk)
        client.delete()
        message = {'detail': 'client deleted successfully'}
        return Response(message) 
    
    if request.method == 'PUT' :
        client=get_object_or_404(Client, id=pk)
        data=request.data


        name = data.get('name', client.name)
      
        mobile_phone = data.get('mobile_phone', client.mobile_phone)
        arabic_name = data.get('arabic_name', client.arabic_name)
        city = data.get('city', client.city)

        client.name = name
        
        client.mobile_phone = mobile_phone
        client.arabic_name = arabic_name
        client.city = city

        client.save()


        message = {'detail': 'Client updated successfully'}
        return Response(message) 


        
        


