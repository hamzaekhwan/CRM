
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

    filterset_fields = [
                        'city',
                    
                        ]
    
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
           

    