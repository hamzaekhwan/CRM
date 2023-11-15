
from rest_framework import generics
from CRMapp.models import *
from CRMapp.maintenanceslift.serializers import *
from CRMapp.authentications.permissions import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse


class MaintenanceLiftListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint ]
    queryset = MaintenanceLift.objects.all()
    serializer_class = MaintenanceLiftSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = [
                        
                        'maintenance_type',
                        'spare_parts',
                        'number_of_visits_per_year',

        ]
    
    search_fields = ['contract__ats',
                     'contract__lift_type',
                     'maintenance_contract_number',
                     'brand',
                     'villa_no']
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': Contract(queryset, many=True).data
        }

        return JsonResponse(data)
           

    