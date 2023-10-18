from .serializers import *

from rest_framework.views import *
from rest_framework.decorators import *
from rest_framework.response import *
from rest_framework.permissions import *
from django.http import JsonResponse
from CRMapp.models import *
from .functions import *
from django.shortcuts import get_object_or_404

@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsAdminUser])
def contract(request,pk=None):
    if request.method == 'POST' :
        data=request.data

        

        ats=data['ats']

        contract_exists = Contract.objects.filter(ats=ats).exists()
        if not contract_exists:
            client_id=data['client_id']
            client=Client.objects.get(id=client_id)

            
           

            

          

           

            lift_type=data['lift_type']

            size=data['size']

            floors=data['floors']

       


            location=data['location']

           

            

            new_conrtract=Contract.objects.create(
                                        ats=ats,
                                        client=client,
                                        lift_type=lift_type,
                                        size=size,
                                        floors=floors,
                                        location=location )
            
           
            
            message = {'detail': 'Contract added successfully'}
            return Response(message)
            

        else:
            message = {'detail': 'Contract with this number already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'GET' :
        if pk is not None:
          
            user = get_object_or_404(Contract, id=pk)
            serializer = Contract(user)
            return Response(serializer.data)
        else:
            query=Contract.objects.all()

            serializer=Contract(query,many=True)
            return Response(serializer.data)
    
    if request.method == 'DELETE' :
        
        contract = get_object_or_404(Contract, id=pk)
        contract.delete()
      
        message = {'detail': 'Admin deleted successfully'}
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
@permission_classes([IsAdminUser])
def contract_phases_by_id(request,pk):

    contract_obj=Contract.objects.get(id=pk)

    query=Phase.objects.filter(contract=contract_obj)
    serializer=PhaseSerializer(query,many=True)
    return JsonResponse(serializer.data,safe=False)

#################################################################################

@api_view(['POST','PUT','DELETE','GET'])
@permission_classes([IsAdminUser])
def note(request,pk=None):
    if request.method == 'POST' :
        data=request.data
        
        
        contract=Contract.objects.get(id=pk)

        note=data['note']
        date=data['date']
        try:
            attachment=request.FILES.get('attachment')
        except:
            attachment=None

        Note.objects.create(contract=contract,
                                        client=contract.client,
                                        note=note,
                                        attachment=attachment,
                                        date=date)
        
        message = {'detail': 'Note added successfully'}
        return Response(message)
    if request.method == 'DELETE' :
        Note.objects.filter(id=pk).delete()
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
@permission_classes([IsAdminUser])
def phase(request,pk=None):
    if request.method == 'POST' :
        data=request.data
        contract_obj=Contract.objects.get(id=pk)

        start_date_new_phase=data['start_date']
        name=data['name']

        new_phase = move_to_specific_phase(contract_obj,start_date_new_phase,name)
        if new_phase:
            message = {'detail': 'move done successfully'}
            return Response(message)
        else:
            message = {'detail': 'there is no phases for this contract'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)



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
@permission_classes([IsAdminUser])
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





        
