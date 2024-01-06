from .serializers import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from CRMapp.models import *
from django.shortcuts import get_object_or_404
from CRMapp.authentications.permissions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@api_view(['POST','PUT','DELETE','GET'])
@permission_classes([IsManager | IsManagerMaint ])
def maintenancelift(request,pk=None):
    if request.method == 'POST' :
        data=request.data
        
        
        contract = get_object_or_404(Contract, id=pk)
        if contract.interest.company_name != "ATLAS" : 
            message = {'detail': 'Maintenance Lift is only for Atlas '}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
            
        maintenance_contract_number=data['maintenance_contract_number']
        maintenance_contract_start_date=data['maintenance_contract_start_date']
        maintenance_contract_end_date=data['maintenance_contract_end_date']

        maintenance_type=data['maintenance_type']
        if maintenance_type not in dict(MAINTAINCANCE_CHOICES).keys():
            message = {'detail': 'you should select Maintenance Type '}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        contract_value=data['contract_value']
        spare_parts=data['spare_parts']
        if spare_parts not in dict(SPARE_PARTS).keys():
            message = {'detail': 'you should select Spare parts '}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        brand=data['brand']
      
        villa_no=data['villa_no']
        handing_over_date=data['handing_over_date']
        number_of_visits_per_year=data['number_of_visits_per_year']
        free_maintenance_expiry_date=data['free_maintenance_expiry_date']
        
        # serializer=ContractSerializer(Contract,many=True)
        # if serializer.data.current_phase=="MAINTENANCE":
        maintenancemift_exist=MaintenanceLift.objects.filter(contract=contract).exists()
        if maintenancemift_exist == False :
            MaintenanceLift.objects.create(contract=contract,
                                        
                                            maintenance_contract_number=maintenance_contract_number,
                                            maintenance_contract_start_date=maintenance_contract_start_date,
                                            maintenance_contract_end_date=maintenance_contract_end_date,
                                            maintenance_type=maintenance_type,
                                            contract_value=contract_value,
                                            spare_parts=spare_parts,
                                            brand=brand,
                                            villa_no=villa_no,
                                            handing_over_date=handing_over_date,
                                            number_of_visits_per_year=number_of_visits_per_year,
                                            free_maintenance_expiry_date=free_maintenance_expiry_date)

        
            message = {'detail': 'MaintenancesLift added successfully'}
            return Response(message)
        
        else :
            message = {'detail': 'this contract already has a MaintenancesLift '}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
             
    if request.method == 'DELETE' :
        query=get_object_or_404(MaintenanceLift, id=pk)
        query.delete()
        message = {'detail': 'MaintenanceLift deleted successfully'}
        return Response(message) 
    if request.method == 'PUT':
        maint_obj = get_object_or_404(MaintenanceLift, id=pk)
        data = request.data

        # Conditions for PUT request data validation
        fields_to_update = [
            'maintenance_contract_number',
            'maintenance_contract_start_date',
            'maintenance_contract_end_date',
            'maintenance_type',
            'contract_value',
            'spare_parts',
            'brand',
            'villa_no',
            'handing_over_date',
            'number_of_visits_per_year',
            'free_maintenance_expiry_date',
        ]

        for field in fields_to_update:
            setattr(maint_obj, field, data.get(field, getattr(maint_obj, field)))

        # Validate maintenance_type
        if maint_obj.maintenance_type not in dict(MAINTAINCANCE_CHOICES).keys():
            return Response({'detail': 'Invalid maintenance type. Please provide a valid maintenance type.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate spare_parts
        if maint_obj.spare_parts not in dict(SPARE_PARTS).keys():
            return Response({'detail': 'Invalid spare parts. Please provide a valid spare parts value.'}, status=status.HTTP_400_BAD_REQUEST)

        maint_obj.save()

        message = {'detail': 'MaintenancesLift updated successfully'}
        return Response(message, status=status.HTTP_200_OK)
  
    if request.method == 'GET' :
        if pk is not None:
            query = get_object_or_404(MaintenanceLift, id=pk)
            serializer = MaintenanceLiftSerializer(query)
            return Response(serializer.data)
        else:
            query = MaintenanceLift.objects.all().order_by('-id')
            serializer = MaintenanceLiftSerializer(query, many=True)
            return Response(serializer.data)

@api_view(['GET']) #pagination api
@permission_classes([IsManager | IsManagerMaint])
def getmaintenancelifts(request):
    query = request.query_params.get('keyword')

    if query is None:
        query = ''

    maintenancelifts = MaintenanceLift.objects.filter(contract__ats__icontains=query).order_by('-id')

    # Get the total count before pagination
    total_count = maintenancelifts.count()

    page = request.query_params.get('page')
    paginator = Paginator(maintenancelifts, 10)

    try:
        maintenancelifts = paginator.page(page)
    except PageNotAnInteger:
        maintenancelifts = paginator.page(1)
    except EmptyPage:
        maintenancelifts = paginator.page(paginator.num_pages)

    if page is None:
        page = 1

    page = int(page)

    serializer = MaintenanceLiftSerializer(maintenancelifts, many=True)

    # Include the total count in the JSON response
    response_data = {
        'maintenancelifts': serializer.data,
        'count': total_count,
        'page': page,
        'pages': paginator.num_pages
    }

    return Response(response_data)