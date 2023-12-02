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
import shortuuid
from CRMapp.functions import convert_base64
from CRMapp.authentications.serializers import UserSerializer
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
                serializer=UserSerializer(user,many=False)
                #Login successful
                return Response({'message': 'Login successful' , "result":serializer.data }, status=200)
            else:
                return Response({'message': 'Login failed, user is an employee'}, status=401)
        else:
            return Response({'message': 'Login failed, please check the entered information'}, status=401)

    return Response({'message': 'Please use a POST request to log in'}, status=400)

@api_view(['POST'])
@permission_classes([ApiKeyPermission])
def maintenance_mobile(request,pk=None):
 
    
    contract = get_object_or_404(Contract, id=pk)
    maintenance_lift=get_object_or_404(MaintenanceLift,contract=contract)
    data=request.data
    
    user_id=data['user_id']
    helper1=data['helper1']
    helper2=data['helper2']
    type_name=data['type_name']
    remarks=data['remarks']
    date=data['date']
    code64_list = data.getlist('check_images')

    technician=User.objects.get(id=user_id).first_name

    s = shortuuid.ShortUUID(alphabet="0123456789abcde")
   

    maintenance=Maintenance.objects.create(contract=contract,
                                maintenance_lift=maintenance_lift,
                                type_name=type_name,
                                remarks=remarks,
                                date=date,
                                technician=technician,
                                helper1=helper1,
                                helper2=helper2
                                    )
    

    for code64 in code64_list:
        otp = s.random(length=12)
        image = convert_base64(code64, data['type_name'], otp)
        CheckImage.objects.create(maintenance=maintenance, image=image)
       

    message = {'detail': 'maint added successfully'}
    return JsonResponse(message,safe=False, status=status.HTTP_200_OK)

@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsManager | IsManagerMaint])
def maintenance_website(request,pk=None):
 
    if request.method == 'POST' :
        contract = get_object_or_404(Contract, id=pk)
        maintenance_lift=get_object_or_404(MaintenanceLift,contract=contract)
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
           
