
from rest_framework import generics
from CRMapp.models import *
from CRMapp.maintenances.serializers import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse



class MaintenanceListView(generics.ListAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = ['type_name']
    
    search_fields = ['contract__interest__client__name',
                     'contract__interest__client__arabic_name',
                     'contract__interest__client__city',
                     'date']
 
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': MaintenanceSerializer(queryset, many=True).data
        }

        return JsonResponse(data)