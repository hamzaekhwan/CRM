
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *
from CRMapp.clients.serializers import *

from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = ['city','inquiry']
    
    search_fields = ['name',
                     'arabic_name',
                     'city',
                     'mobile_phone',
                     ]
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': ClientSerializer(queryset, many=True).data
        }

        return JsonResponse(data)
           

class InterestListView(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = ['client__city','client__inquiry','company_name']
    
    search_fields = ['client__name',
                     'client__arabic_name',
                     'client__city',
                     'client__mobile_phone',
                     'company_name'
                     ]
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': InterestSerializer(queryset, many=True).data
        }

        return JsonResponse(data)