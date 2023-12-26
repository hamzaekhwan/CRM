
from .serializers import *
from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from CRMapp.authentications.permissions import *
from django.http import JsonResponse
from CRMapp.models import *
from django.shortcuts import get_object_or_404
from CRMapp.functions import export_to_csv , export_to_excel ,export_to_pdf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from CRMapp.validators import phone_regex
@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def client(request,pk=None):
    if request.method == 'POST' :
        data=request.data

        name=data['name']
        mobile_phone=data['mobile_phone']
        try:
                phone_regex(mobile_phone)
        except:
                message = {'detail': "Phone number must be entered in the format: '+9715Xxxxxxxx'"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        client_exists = Client.objects.filter(name__icontains=name).exists() or Client.objects.filter(mobile_phone=mobile_phone).exists()
        if not client_exists:
            
            
            arabic_name=data['arabic_name']
            city=data['city']
            # inquiry=data['inquiry']
            date=data['date']
            company_name=data['company_name']
            client=Client.objects.create(name=name,
                                mobile_phone=mobile_phone,
                                arabic_name=arabic_name,
                                city=city,
      
                                date=date )
            
            
            Interest.objects.create(client=client,company_name=company_name)

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
            query=Client.objects.all().order_by('-id')
            serializer=ClientSerializer(query,many=True)
            return JsonResponse(serializer.data,safe=False)
    
    if request.method == 'DELETE' :
        client=get_object_or_404(Client, id=pk)
        client.delete()
        message = {'detail': 'client deleted successfully'}
        return Response(message,status=status.HTTP_204_NO_CONTENT)
    
    if request.method == 'PUT' :
        client=get_object_or_404(Client, id=pk)
        data=request.data


        name = data.get('name', client.name)
      
        mobile_phone = data.get('mobile_phone', client.mobile_phone)
        
        try:
                phone_regex(mobile_phone)
        except:
                message = {'detail': "Phone number must be entered in the format: '+9715Xxxxxxxx'"}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

        arabic_name = data.get('arabic_name', client.arabic_name)
        city = data.get('city', client.city)

        client.name = name
        
        client.mobile_phone = mobile_phone
        client.arabic_name = arabic_name
        client.city = city

        client.save()


        message = {'detail': 'Client updated successfully'}
        return Response(message) 

    
 

@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def interest(request,pk=None):
    if request.method == 'POST' :
        client = get_object_or_404(Client, id=pk)
        data = request.data

        company_name = data['company_name']
        # inquiry=data['inquiry']
        interest_exist=Interest.objects.filter(client=client,company_name=company_name)
        if not interest_exist:
            Interest.objects.create(
                client=client,
                company_name=company_name,
              
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
            query=Interest.objects.all().order_by('-id')
            serializer=InterestSerializer(query,many=True)
            return JsonResponse(serializer.data,safe=False)
        
    if request.method == 'PUT' :
        interest=get_object_or_404(Interest, id=pk)
        client=interest.client
        data=request.data


        company_name = data.get('company_name', interest.company_name)
        # inquiry = data.get('inquiry', interest.inquiry)

        interest_exist=Interest.objects.filter(client=client,company_name=company_name).exclude(id=pk)
        if not interest_exist :
            interest.company_name=company_name
           
            interest.save()
            message = {'detail': 'interest updated successfully'}
            return Response(message) 

        else:
            message = {'detail': 'client with this interest already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        interest = get_object_or_404(Interest, id=pk)
        
        # Check if this is the last interest associated with the client
        client = interest.client
        if client.interest_set.count() == 1:
            message = {'detail': 'Cannot delete the last interest associated with the client.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        # If not the last interest, proceed with deletion
        interest.delete()
        message = {'detail': 'Interest deleted successfully'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])  # You can customize permissions here
def reminder(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            reminder = get_object_or_404(Reminder, id=pk)
            serializer = ReminderSerializer(reminder)
            return Response(serializer.data)
        else:
            reminders = Reminder.objects.all().order_by('-id')
            serializer = ReminderSerializer(reminders, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        client = get_object_or_404(Client, id=pk)
        data = request.data

        # Assuming you have 'company_name' and 'inquiry' in your Reminder model
        message = data.get('message')
        reminder_datetime = data.get('reminder_datetime')
        admin=request.user

        reminder_exist = Reminder.objects.filter(client=client, reminder_datetime=reminder_datetime)
        if not reminder_exist:
            Reminder.objects.create(
                client=client,
                admin=admin,
                message=message,
                reminder_datetime=reminder_datetime,
                notification_sent=False,
            )

            message = {'detail': 'reminder added successfully'}
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            message = {'detail': 'client with this reminder already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        reminder = get_object_or_404(Reminder, id=pk)
        data = request.data

        reminder.message=data.get('message', reminder.message)
        reminder.reminder_datetime=data.get('reminder_datetime', reminder.reminder_datetime)

        message = {'detail': 'reminder updated successfully'}
        return Response(message, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        reminder = get_object_or_404(Reminder, id=pk)
        reminder.delete()
        message = {'detail': 'reminder deleted successfully'}
        return Response(message,status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def getclients(request):
    
    query = request.query_params.get('keyword')
    
    if query == None:
        query = ''

    clients = Client.objects.filter(
        name__icontains=query).order_by('-id')

    page = request.query_params.get('page')
    paginator = Paginator(clients, 1)

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    
    serializer = ClientSerializer(clients, many=True)
    return Response({'clients': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def getinterests(request):
    query = request.query_params.get('keyword')
    
    if query == None:
        query = ''

    interests = Interest.objects.filter(
        client__name__icontains=query).order_by('-id')

    page = request.query_params.get('page')
    paginator = Paginator(interests, 10)

    try:
        interests = paginator.page(page)
    except PageNotAnInteger:
        interests = paginator.page(1)
    except EmptyPage:
        interests = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    
    serializer = InterestSerializer(interests, many=True)
    return JsonResponse({'interests': serializer.data, 'page': page, 'pages': paginator.num_pages})

# @api_view(['POST'])
# def export_file(request, file_type):
#     data=request.data
#     client_ids=request.data.get('client_ids', [])
#     queryset = Client.objects.filter(client__id__in=client_ids)

#     if file_type == 'excel':
#         excel_file = export_to_excel(queryset)
#         response = Response(excel_file, content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="client_data.xlsx"'
#         return response
#     elif file_type == 'pdf':
#         pdf_file = export_to_pdf(queryset)
#         response = Response(pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="exported_data.pdf"'
#         return response

#     elif file_type == 'csv':
#         csv_file = export_to_csv(queryset)
#         response = Response(csv_file, content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
#         return response

#     # في حالة عدم اختيار نوع الملف المدعوم
#     return Response({'detail': 'Unsupported file type.'}, status=status.HTTP_400_BAD_REQUEST)
        

