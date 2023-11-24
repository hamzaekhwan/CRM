from .serializers import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from django.http import JsonResponse
from CRMapp.models import *
from django.shortcuts import get_object_or_404
from CRMapp.authentications.permissions import *
from django.contrib.auth import authenticate, login
############# login for mobile
@api_view(['POST'])
def login_mobile(request):
    if request.method == 'POST':
        username_or_email = request.data.get('username')
        password = request.data.get('password')

        # Check if the username or email exists in the database
        user = None
        if '@' in username_or_email:
            # If the input is an email
            user = authenticate(request, email=username_or_email, password=password)
        else:
            # If the input is a username
            user = authenticate(request, username=username_or_email, password=password)

        # Check the success of authentication
        userprofile=UserProfile.objects.get(user=user)
        if user is not None and not userprofile.isEmp:
            login(request, user)
            return Response({'message': 'Login successful'},status=200)
        else:
            return Response({'message': 'Login failed, please check the entered information'},status=401)

    return Response({'message': 'Please use a POST request to log in'},status=400)


@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsManager | IsManagerMaint | IsMaint])
def maintenance(request,pk=None):
 
    if request.method == 'POST' :
        contract = get_object_or_404(Contract, id=pk)
      
        data=request.data
       
        data = request.data
        type_name=data['type_name']
        remarks=data['remarks']
        date=data['date']
        signature_of_client=request.FILES.get('signature_of_client')
        signature_of_supervisor=request.FILES.get('signature_of_supervisor')
        signature_of_technician=request.FILES.get('signature_of_technician')

        maintenance=Maintenance.objects.create(contract=contract,
                             
                                    type_name=type_name,
                                    remarks=remarks,
                                    date=date,
                                    signature_of_client=signature_of_client,
                                    signature_of_supervisor=signature_of_supervisor,
                                    signature_of_technician=signature_of_technician )
        
        mysections=data['mysections']
        mysections = eval(mysections)
        for key, value in mysections.items():
            if hasattr(Maintenance, key):
                Maintenance.objects.filter(id=maintenance.id).update(**{key: value})



        message = {'detail': 'maint added successfully'}
        return JsonResponse(message,safe=False, status=status.HTTP_200_OK)
    
    if request.method == 'GET' :  
        if pk is not None:
            maintenance = get_object_or_404(Maintenance, id=pk)
            
            serializer = MaintenanceSerializer(maintenance)
            return JsonResponse(serializer.data,safe=False)
        else:
            maintenances = Maintenance.objects.all()
            serializer = MaintenanceSerializer(maintenances, many=True)
            return JsonResponse(serializer.data,safe=False)                 

    if request.method == 'DELETE' :
        maintenance = get_object_or_404(Maintenance, id=pk)
        maintenance.delete()
        message = {'detail': 'Maintenance deleted successfully'}
        return Response(message)

    if request.method == 'PUT' :
        maintenance_obj = get_object_or_404(Maintenance, id=pk)
        data = request.data
        for key,value in data.items():
            if hasattr(Maintenance, key):
                    Maintenance.objects.filter(id=maintenance_obj.id).update(**{key: value})

        message = {'detail': 'Maintenance updated successfully'}
        return JsonResponse(message,safe=False)        
