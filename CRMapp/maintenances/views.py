from .serializers import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from django.http import JsonResponse
from CRMapp.models import *
from django.shortcuts import get_object_or_404
from CRMapp.authentications.permissions import *

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
        return JsonResponse(message, status=status.HTTP_200_OK)
    
    if request.method == 'GET' :  
        if pk is not None:
            maintenance = get_object_or_404(Maintenance, id=pk)
            
            serializer = MaintenanceSerializer(maintenance)
            return JsonResponse(serializer.data)
        else:
            maintenances = Maintenance.objects.all()
            serializer = MaintenanceSerializer(maintenances, many=True)
            return JsonResponse(serializer.data)                 

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
        return JsonResponse(message)        
