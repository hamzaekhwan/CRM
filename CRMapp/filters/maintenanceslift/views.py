
from rest_framework import generics
from CRMapp.models import *
from CRMapp.maintenanceslift.serializers import *
from CRMapp.authentications.permissions import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class MaintenanceLiftListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint ]
    queryset = MaintenanceLift.objects.all().order_by('-id')
    serializer_class = MaintenanceLiftSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = [
                        
                        'maintenance_type',
                        'spare_parts',
                        'number_of_visits_per_year',
                        "contract__interest__client__city",
                        "contract__interest__company_name",
                        "contract__floors",
                        "contract__lift_type",
                        'contract__signed',]
    
    search_fields = ['contract__ats',
                     'contract__lift_type',
                     'maintenance_contract_number',
                     'brand',
                     'villa_no']
    
    ordering_fields = [
        'maintenance_type',
        'maintenance_contract_number',
        'brand',
        'number_of_visits_per_year',
        'contract__interest__client__city',
        'contract__interest__company_name',
        'contract__floors',
        'contract__lift_type',
        'maintenance_contract_end_date',
        'handing_over_date',
        'free_maintenance_expiry_date',
        'contract_value',
        'villa_no',
        'maintenance_contract_start_date',  # Add the field for sorting
    ]

    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        ordering = request.query_params.get('ordering', '-id')  # Default to sorting by '-id' if no ordering is specified
        queryset = queryset.order_by(ordering)

        page = request.query_params.get('page')
        paginator = Paginator(queryset, 10)

        try:
            maintenancelifts = paginator.page(page)
        except PageNotAnInteger:
            maintenancelifts = paginator.page(1)
        except EmptyPage:
            maintenancelifts = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        
        serializer = MaintenanceLiftSerializer(maintenancelifts, many=True)
        return JsonResponse({'MaintenanceLifts': serializer.data, 'page': page, 'pages': paginator.num_pages})
           

    