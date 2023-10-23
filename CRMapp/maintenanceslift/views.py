from .serializers import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from CRMapp.models import *
from django.shortcuts import get_object_or_404

@api_view(['POST','PUT','DELETE','GET'])
@permission_classes([IsAdminUser])
def maintenancelift(request,pk=None):
    if request.method == 'POST' :
        data=request.data
        
        
        contract = get_object_or_404(Contract, id=pk)
        maintenance_contract_number=data['maintenance_contract_number']
        maintenance_contract_start_date=data['maintenance_contract_start_date']
        maintenance_contract_end_date=data['maintenance_contract_end_date']

        maintenance_type=data['maintenance_type']
        contract_value=data['contract_value']
        spare_parts=data['spare_parts']
        brand=data['brand']
      
        villa_no=data['villa_no']
        handing_over_date=data['handing_over_date']
        number_of_visits_per_year=data['number_of_visits_per_year']
        free_maintenance_expiry_date=data['free_maintenance_expiry_date']

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
    if request.method == 'DELETE' :
        query=get_object_or_404(MaintenanceLift, id=pk)
        query.delete()
        message = {'detail': 'MaintenanceLift deleted successfully'}
        return Response(message) 
    if request.method == 'PUT' :
        maint_obj = get_object_or_404(MaintenanceLift, id=pk)
        data = request.data

        
        maint_obj.maintenance_contract_number = data.get('maintenance_contract_number', maint_obj.maintenance_contract_number)
        maint_obj.maintenance_contract_start_date = data.get('maintenance_contract_start_date', maint_obj.maintenance_contract_start_date)
        maint_obj.maintenance_contract_end_date = data.get('maintenance_contract_end_date', maint_obj.maintenance_contract_end_date)
        maint_obj.maintenance_type = data.get('maintenance_type', maint_obj.maintenance_type)
        maint_obj.contract_value = data.get('contract_value', maint_obj.contract_value)
        maint_obj.spare_parts = data.get('spare_parts', maint_obj.spare_parts)
        maint_obj.brand = data.get('brand', maint_obj.brand)
        maint_obj.villa_no = data.get('villa_no', maint_obj.villa_no)
        maint_obj.handing_over_date = data.get('handing_over_date', maint_obj.handing_over_date)
        maint_obj.number_of_visits_per_year = data.get('number_of_visits_per_year', maint_obj.number_of_visits_per_year)
        maint_obj.free_maintenance_expiry_date = data.get('free_maintenance_expiry_date', maint_obj.free_maintenance_expiry_date)
        

        maint_obj.save()

        message = {'detail': 'MaintenancesLift updated successfully'}
        return Response(message, status=status.HTTP_200_OK)
  
    if request.method == 'GET' :
        if pk is not None:
            query = get_object_or_404(MaintenanceLift, id=pk)
            serializer = MaintenanceLiftSerializer(query)
            return Response(serializer.data)
        else:
            query = MaintenanceLift.objects.all()
            serializer = MaintenanceLiftSerializer(query, many=True)
            return Response(serializer.data)
