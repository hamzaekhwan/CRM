
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *
from CRMapp.clients.serializers import *

from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse


class ElevatorContracListView(generics.ListAPIView):
    queryset = ElevatorContract.objects.all()
    serializer_class = ElevatorContractSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = [
                        'type_maintenance',
                        'type',
                        'floors',
                        'brand',
                        'number_of_visits_per_year']
    
    search_fields = ['client__name',
                     'client__arabic_name',
                     'client__city',
                     'maintenance_contract_number',
                     'maintenance_contract_start_date',
                     'villa_no']
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': ElevatorContractSerializer(queryset, many=True).data
        }

        return JsonResponse(data)
           

    