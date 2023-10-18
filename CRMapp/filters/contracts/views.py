
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *

from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse


class ContractListView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = [
                        
                        'lift_type',
                        'floors',
        ]
    
    search_fields = ['client__name',
                     'client__arabic_name',
                     'client__city',
                     'ats']
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': Contract(queryset, many=True).data
        }

        return JsonResponse(data)
           

    