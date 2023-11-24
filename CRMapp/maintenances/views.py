from .serializers import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from django.http import JsonResponse
from CRMapp.models import *
from django.shortcuts import get_object_or_404
from CRMapp.authentications.permissions import *
from django.contrib.auth import login
from django.db.models import Q

############# login for mobile
@api_view(['POST'])
def login_mobile(request):
    if request.method == 'POST':
        username_or_email = request.data.get('username')
        password = request.data.get('password')

        try:
            # Try to get the user by username or email
            user = User.objects.get(Q(username=username_or_email) | Q(email__iexact=username_or_email))
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            try:
                # Check the existence of UserProfile
                userprofile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                return Response({'message': 'UserProfile does not exist for the authenticated user'}, status=401)

            if not userprofile.isEmp:
                login(request, user)
                return Response({'message': 'Login successful'}, status=200)
            else:
                return Response({'message': 'Login failed, user is an employee'}, status=401)
        else:
            return Response({'message': 'Login failed, please check the entered information'}, status=401)

    return Response({'message': 'Please use a POST request to log in'}, status=400)


@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsManager | IsManagerMaint | IsMaint])
def maintenance(request,pk=None):
 
    if request.method == 'POST' :
        contract = get_object_or_404(Contract, id=pk)
        maintenance_lift=MaintenanceLift.objects.get_or_create(contract=contract)
        data=request.data
       
        type_name=data['type_name']
        remarks=data['remarks']
        date=data['date']
        check_image=request.FILES.get('check_image')
       
        maintenance=Maintenance.objects.create(contract=contract,
                                    maintenance_lift=maintenance_lift,
                                    type_name=type_name,
                                    remarks=remarks,
                                    date=date,
                                    check_image=check_image,
                                     )
    
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

        
        maintenance_obj.type_name = data.get('type_name', maintenance_obj.type_name)
        maintenance_obj.remarks = data.get('remarks', maintenance_obj.remarks)
        maintenance_obj.date = data.get('date', maintenance_obj.date)

        check_image = request.FILES.get('check_image', None)
        if check_image is not None:
            maintenance_obj.check_image = check_image

       
        
        

        maintenance_obj.save()

        message = {'detail': 'Maintenance updated successfully'}
        return Response(message, status=status.HTTP_200_OK)
           
