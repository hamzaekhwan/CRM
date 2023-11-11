
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
        mobile_phone=data['mobile_phone']
        client_exists = Client.objects.filter(name__icontains=name).exists() or Client.objects.filter(mobile_phone=mobile_phone).exists()
        if not client_exists:
            
            
            arabic_name=data['arabic_name']
            city=data['city']
            inquiry=data['inquiry']
            date=data['date']
            company_name=data['company_name']
            client=Client.objects.create(name=name,
                                mobile_phone=mobile_phone,
                                arabic_name=arabic_name,
                                city=city,
      
                                date=date )
            
            
            Interest.objects.create(client=client,company_name=company_name,inquiry=inquiry)

            message = {'detail': 'Client added successfully'}
            return Response(message) 
        else:
            message = {'detail': 'client with this name already exists'}
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

    
 

@api_view(['POST','GET','PUT'])
@permission_classes([IsAdminUser])
def interest(request,pk=None):
    if request.method == 'POST' :
        client = get_object_or_404(Client, id=pk)
        data = request.data

        company_name = data['company_name']
        inquiry=data['inquiry']
        interest_exist=Interest.objects.filter(client=client,company_name=company_name)
        if not interest_exist:
            Interest.objects.create(
                client=client,
                company_name=company_name,
                inquiry=inquiry
            )

            message = {'detail': 'interest added successfully'}
            return Response(message)
        else:
            message = {'detail': 'client with this interest already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET' :
        if pk is not None:
            user = get_object_or_404(Interest, id=pk)
            serializer = InterestSerializer(user)
            return Response(serializer.data)
        else:
            query=Interest.objects.all()
            serializer=InterestSerializer(query,many=True)
            return JsonResponse(serializer.data,safe=False)
        
    if request.method == 'PUT' :
        interest=get_object_or_404(Interest, id=pk)
        client=interest.client
        data=request.data


        company_name = data.get('company_name', interest.company_name)
        inquiry = data.get('inquiry', interest.inquiry)
        
        interest_exist=Interest.objects.filter(client=client,company_name=company_name)
        if not interest_exist :
            interest.company_name=company_name
            interest.inquiry=inquiry
            interest.save()
            message = {'detail': 'interest updated successfully'}
            return Response(message) 

        else:
            message = {'detail': 'client with this interest already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)



            
  
