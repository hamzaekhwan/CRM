from .serializers import *

from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from django.http import JsonResponse
from CRMapp.models import *
from django.shortcuts import get_object_or_404
from django.utils import timezone
from CRMapp.authentications.permissions import *
from CRMapp.maintenances.serializers import MaintenanceSerializer

@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def contract(request,pk=None):
    if request.method == 'POST' :
        data=request.data

        

        ats=data['ats']
        interest_id=data['interest_id']
        contract_exists = Contract.objects.filter(ats=ats).exists()
        if not contract_exists:

            interest=get_object_or_404(Interest, id=interest_id)


            lift_type=data['lift_type']

            size=data['size']

            floors=data['floors']

            location=data['location']


            new_conrtract=Contract.objects.create(
                                        ats=ats,
                                        interest=interest,
                                        lift_type=lift_type,
                                        size=size,
                                        floors=floors,
                                        location=location )
            
           
            
            message = {'detail': 'Contract added successfully'}
            return Response(message)
            

        else:
            message = {'detail': 'Contract with this Ats already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET' :
        if pk is not None:
          
            user = get_object_or_404(Contract, id=pk)
            serializer = ContractSerializer(user)
            return Response(serializer.data)
        else:
            query=Contract.objects.all()

            serializer=ContractSerializer(query,many=True)
            return Response(serializer.data)
    
    if request.method == 'DELETE' :
        
        contract = get_object_or_404(Contract, id=pk)
        contract.delete()
      
        message = {'detail': 'Contract deleted successfully'}
        return Response(message)
    
    if request.method == 'PUT' :
        contract = get_object_or_404(Contract, id=pk)
        data = request.data
        
        contract.ats=data.get('ats', contract.ats)
        contract.lift_type=data.get('lift_type', contract.lift_type)
        contract.size = data.get('size', contract.size)
        contract.floors = data.get('floors', contract.floors)
        contract.location = data.get('location', contract.location)

        contract.save()

        message = {'detail': 'contract updated successfully'}
        return Response(message, status=status.HTTP_200_OK)
    
               
@api_view(['GET'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def contract_phases_by_id(request,pk):

    contract = get_object_or_404(Contract, id=pk)

    query=Phase.objects.filter(contract=contract)
    serializer=PhaseSerializer(query,many=True)
    return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
@permission_classes([IsManager | IsManagerMaint])
def maintenancelift_contract_by_id(request,pk):

    contract = get_object_or_404(Contract, id=pk)

    query=MaintenanceLift.objects.filter(contract=contract)
    serializer=ContractMaintenanceSerializer(query,many=True)
    return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
@permission_classes([IsManager | IsManagerMaint])
def maintenance_contract_by_id(request,pk):

    contract = get_object_or_404(Contract, id=pk)

    query=Maintenance.objects.filter(contract=contract)
    serializer=MaintenanceSerializer(query,many=True)
    return JsonResponse(serializer.data,safe=False)

#api to get contracts by client id
@api_view(['GET'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def client(request,pk=None):
   

    client=get_object_or_404(Client,id=pk)
    interests=Interest.objects.filter(client=client)

    
    contract=Contract.objects.filter(interest__in=interests)
       
        

    serializer=ContractSerializer(contract,many=True)
    return JsonResponse(serializer.data,safe=False)
#################################################################################

@api_view(['POST','PUT','DELETE','GET'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def note(request,pk=None):
    if request.method == 'POST' :
        data=request.data
        
        
        contract = get_object_or_404(Contract, id=pk)

        note=data['note']
        date=data['date']
        try:
            attachment=request.FILES.get('attachment')
        except:
            attachment=None

        Note.objects.create(contract=contract,
                                        
                                        note=note,
                                        attachment=attachment,
                                        date=date)
        
        message = {'detail': 'Note added successfully'}
        return Response(message)
    if request.method == 'DELETE' :
        query=get_object_or_404(Note, id=pk)
        query.delete()
        message = {'detail': 'Note deleted successfully'}
        return Response(message) 
    if request.method == 'PUT' :
        note_obj = get_object_or_404(Note, id=pk)
        data = request.data

        
        note_obj.note = data.get('note', note_obj.note)
        note_obj.date = data.get('date', note_obj.date)
        
        
        attachment = request.FILES.get('attachment', None)
        if attachment is not None:
            note_obj.attachment = attachment

        note_obj.save()

        message = {'detail': 'Note updated successfully'}
        return Response(message, status=status.HTTP_200_OK)
  
    if request.method == 'GET' :
        if pk is not None:
            note = get_object_or_404(Note, id=pk)
            serializer = NoteSerializer(note)
            return Response(serializer.data)
        else:
            notes = Note.objects.all()
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)

#################################################################################


@api_view(['POST','PUT','DELETE','GET'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def phase(request,pk=None):
    if request.method == 'POST' :
        contract = get_object_or_404(Contract, id=pk)

        data=request.data
        start_date_new_phase=data['start_date'] 
        name=data['name']

        if name not in [choice[1] for choice in PHASES_NAME]:
            message = {'detail': 'this phase name doesnt exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        existing_phase = Phase.objects.filter(contract=contract, Name=name).first()
        if existing_phase:
            message = {'detail': 'phase with this name already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        


        Phase.objects.create(
            contract=contract,
            Name=name,
            isActive=True,
            start_date=start_date_new_phase,
        )

        return JsonResponse({'detail': 'phase created successfully'})

    if request.method == 'PUT' :
        phase_obj = get_object_or_404(Phase, id=pk)
        data = request.data

       
        phase_obj.start_date = data.get('start_date', phase_obj.start_date)
        phase_obj.end_date = data.get('end_date', phase_obj.end_date)

        phase_obj.save()

        message = {'detail': 'Phase updated successfully'}
        return Response(message, status=status.HTTP_200_OK)
    
    if request.method == 'DELETE' :
        phase=get_object_or_404(Phase, id=pk)
        phase.delete()
        message = {'detail': 'Phase deleted successfully'}
        return Response(message)

    if request.method =="GET":
        if pk is not None:
            phase = get_object_or_404(Phase, id=pk)
            serializer = PhaseSerializer(phase)
            return Response(serializer.data)
        else:
            phases = Phase.objects.all()
            serializer = PhaseSerializer(phases, many=True)
            return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsManager | IsManagerMaint | IsEmp])
def end_phase(request,pk):
    
    Phase.objects.filter(id=pk).update(isActive=False,end_date=timezone.now())
    message = {'detail': 'phase ended successfully'}
    return Response(message)



# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def auto_change_phase(request):
#     data=request.data
    
#     contract_id=data['contract_id']
#     contract_obj=ElevatorContract.objects.get(id=contract_id)

#     start_date_new_phase=data['start_date']
    
#     new_phase = move_to_next_phase(contract_obj,start_date_new_phase)
#     if new_phase:
#         message = {'detail': 'move done successfully'}
#         return Response(message)
#     else:
#         message = {'detail': 'there is no more phases'}
#         return Response(message, status=status.HTTP_400_BAD_REQUEST)





        
