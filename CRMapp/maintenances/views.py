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
from CRMapp.maintenances.pdfs_creator import create_report
from io import BytesIO
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
def maintenance_mobile(request, pk=None):
    contract = get_object_or_404(Contract, id=pk)
    maintenance_lift = get_object_or_404(MaintenanceLift, contract=contract)

    client_name = contract.interest.client.name    
    client_mobile_phone = contract.interest.client.mobile_phone 
    client_city = contract.interest.client.city 
    ats = contract.ats
    
    data = request.data
    
    user_id = data['user_id']
    technician = User.objects.get(id=user_id).first_name

    helper1 = data['helper1']
    helper2 = data['helper2']
    type_name = data['type_name']
    remarks = data['remarks']
    date = data['date']
    
    # Signatures section
  
    signatures_base64 = data["signatures"]  ## 0-CLIENT NAME 1- client signature 2- TECHNICIAN Signature 
    
    
    # Check Images
    code64_list = data["check_images"]
    
    # Create Maintenance instance
    maintenance = Maintenance.objects.create(
        contract=contract,
        maintenance_lift=maintenance_lift,
        type_name=type_name,
        remarks=remarks,
        date=date,
        technician=technician,
        helper1=helper1,
        helper2=helper2
    )
    
    # Create Check Images
    if len(code64_list)!=0 :
        s = shortuuid.ShortUUID(alphabet="0123456789abcde")
        for code64 in code64_list:
            otp = s.random(length=12)
            image = convert_base64(code64, type_name, otp)
            CheckImage.objects.create(maintenance=maintenance, image=image)
    
    # Create PDF Maintenance Contract
    pdf_maintenance_contract = PdfMaintenanceContract.objects.create(maintenance=maintenance)
    report_number = pdf_maintenance_contract.id
    
    
    sections_data=data['sections_data']

    pdf_file = create_report(
        sections_data,
        date,
        str(report_number),
        client_city,
        ats,
        client_name,
        client_mobile_phone,
        remarks,
        signatures_base64,
    )
    
    buffer = BytesIO(pdf_file)

    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    unique_filename = "{}_{}maintenance_report.pdf".format(client_name, timestamp)
    pdf_maintenance_contract.file.save(unique_filename, buffer)

    message = {'detail': 'Maintenance added successfully'}
    return Response(message, status=status.HTTP_200_OK)

@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsManager | IsManagerMaint])
def maintenance_website(request,pk=None):
 
    # if request.method == 'POST' :
    #     contract = get_object_or_404(Contract, id=pk)
    #     client_name = contract.interest.client.name    
    #     client_mobile_phone = contract.interest.client.mobile_phone 
    #     client_city = contract.interest.client.city 
    #     ats = contract.ats

    #     maintenance_lift=get_object_or_404(MaintenanceLift,contract=contract)
    #     data=request.data
       
    #     type_name=data['type_name']
    #     remarks=data['remarks']
    #     date=data['date']
    #     technician=data['technician']
    #     helper1=data['helper1']
    #     helper2=data['helper2']
    #     check_images=request.FILES.getlist('check_images')

    #     signatures=request.FILES.getlist('signatures') ## 0-TECHNICIAN Signature 1-CLIENT Signature  2-SUPERVISOR Signature
       
    #     maintenance=Maintenance.objects.create(contract=contract,
    #                                 maintenance_lift=maintenance_lift,
    #                                 type_name=type_name,
    #                                 remarks=remarks,
    #                                 date=date,
    #                                 technician=technician,
    #                                 helper1=helper1,
    #                                 helper2=helper2
    #                                 )
        
    #     for image in check_images:
       
    #         CheckImage.objects.create(maintenance=maintenance, image=image)

    #     pdf_maintenance_contract = PdfMaintenanceContract.objects.create(maintenance=maintenance)
    #     report_number = pdf_maintenance_contract.id
        
    #     s = shortuuid.ShortUUID(alphabet="0123456789abcde")
    #     otp = s.random(length=12)
        
    #     sections_data=data['sections_data']
    #     pdf_file = create_report(
    #         sections_data,
    #         date,
    #         report_number,
    #         client_city,
    #         ats,
    #         client_name,
    #         client_mobile_phone,
    #         remarks,
    #         signatures,
    #         output_file="{}_{}maintenance_report.pdf".format(client_name, otp)
    #     )
        
    #     pdf_maintenance_contract.file = pdf_file
    #     pdf_maintenance_contract.save()

 
    
    #     message = {'detail': 'maint added successfully'}
    #     return JsonResponse(message,safe=False, status=status.HTTP_200_OK)
    
    if request.method == 'GET' :  
        if pk is not None:
            maintenance = get_object_or_404(Maintenance, id=pk)
            
            serializer = MaintenanceSerializer(maintenance)
            return JsonResponse(serializer.data,safe=False)
        else:
            maintenances = Maintenance.objects.all().order_by('-id')
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

        maintenance_obj.technician = data.get('technician', maintenance_obj.technician)
        maintenance_obj.helper1 = data.get('helper1', maintenance_obj.helper1)
        maintenance_obj.helper2 = data.get('helper2', maintenance_obj.helper2)




       
        
        

        maintenance_obj.save()

        message = {'detail': 'Maintenance updated successfully'}
        return Response(message, status=status.HTTP_200_OK)

@api_view(['GET']) #pagination api
@permission_classes([IsManager | IsManagerMaint])
def getmaintenances(request):
    query = request.query_params.get('keyword')
    
    if query == None:
        query = ''

    maintenances = Maintenance.objects.filter(
        contract__ats__icontains=query).order_by('-id')

    page = request.query_params.get('page')
    paginator = Paginator(maintenances, 10)

    try:
        maintenances = paginator.page(page)
    except PageNotAnInteger:
        maintenances = paginator.page(1)
    except EmptyPage:
        maintenances = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    
    serializer = MaintenanceSerializer(maintenances, many=True)
    return Response({'maintenances': serializer.data, 'page': page, 'pages': paginator.num_pages})
        
@api_view(['POST','GET','DELETE'])
@permission_classes([IsManager | IsManagerMaint])
def image(request,pk=None):
    if request.method == 'POST' :
        maintenance = get_object_or_404(Maintenance, id=pk)
        data=request.data

        check_images=request.FILES.getlist('check_images')
        
        for image in check_images:
       
            CheckImage.objects.create(maintenance=maintenance, image=image)

        message = {'detail': 'image added successfully'}
        return JsonResponse(message,safe=False, status=status.HTTP_200_OK)    
    
    if request.method == 'DELETE':
        check_image = get_object_or_404(CheckImage, id=pk)

        check_image.delete()

        message = {'detail': 'Image deleted successfully'}
        return JsonResponse(message, safe=False, status=status.HTTP_200_OK)

    
    if request.method == 'GET' :  
       
        check_image = get_object_or_404(CheckImage, id=pk)
        
        serializer = CheckImageSerializer(check_image)
        return JsonResponse(serializer.data,safe=False)  

