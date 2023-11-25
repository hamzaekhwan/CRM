
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *

from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from CRMapp.authentications.permissions import *

class ContractListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint | IsEmp | ApiKeyPermission ]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = [
                        'lift_type',
                        'floors',
                        'interest__company_name',
                        'interest__client__city',]
    
    search_fields = ['interest__client__name',
                     'interest__client__mobile_phone',
                     'interest__client__arabic_name',
                     'interest__client__city',
                     'interest__company_name',
                     'ats',
                     'location',]
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': ContractSerializer(queryset, many=True).data
        }

        return JsonResponse(data)
           

class ContractPhaseListView(generics.ListAPIView):    
    permission_classes = [IsManager | IsManagerMaint | IsEmp]
    queryset = Phase.objects.all()
    serializer_class = PhaseSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = [
                        'contract__lift_type',
                        'contract__floors',
                        'contract__interest__company_name',
                        'contract__interest__client__city',
                        'Name']
    
    search_fields = ['contract__interest__client__name',
                     'contract__interest__client__mobile_phone',
                     'contract__interest__client__arabic_name',
                     'contract__interest__client__city',
                     'contract__interest__company_name',
                     'contract__ats',
                     'contract__location',
                     'Name']
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': PhaseSerializer(queryset, many=True).data
        }

        return JsonResponse(data)
           