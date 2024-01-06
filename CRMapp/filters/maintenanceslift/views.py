
from rest_framework import generics
from CRMapp.models import *
from CRMapp.maintenanceslift.serializers import *
from CRMapp.authentications.permissions import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_filters import FilterSet, DateFromToRangeFilter

class MaintenanceLiftFilter(FilterSet):
    maintenance_contract_start_date = DateFromToRangeFilter()
    maintenance_contract_end_date = DateFromToRangeFilter()
    handing_over_date = DateFromToRangeFilter()
    free_maintenance_expiry_date=DateFromToRangeFilter()
    class Meta:
        model = MaintenanceLift
        fields = [
            'maintenance_type',
            'spare_parts',
            'number_of_visits_per_year',
            "contract__interest__client__city",
            "contract__interest__company_name",
            "contract__floors",
            "contract__lift_type",
            'contract__signed',
            'maintenance_contract_start_date',
            'maintenance_contract_end_date',
            'handing_over_date',
            'free_maintenance_expiry_date'
            # ... add other fields here if needed ...
        ]

class MaintenanceLiftListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint]
    queryset = MaintenanceLift.objects.all().order_by('-id')
    serializer_class = MaintenanceLiftSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MaintenanceLiftFilter



    search_fields = [
        'contract__ats',
        'contract__lift_type',
        'contract__sales_name',
        'maintenance_contract_number',
        'brand',
        'villa_no',
    ]

    ordering_fields = [
        'maintenance_type',
        'maintenance_contract_number',
        'brand',
        'number_of_visits_per_year',
        'contract__ats',
        'contract__interest__client__city',
        'contract__interest__company_name',
        'contract__floors',
        'contract__lift_type',
        'maintenance_contract_end_date',
        'handing_over_date',
        'free_maintenance_expiry_date',
        'contract_value',
        'villa_no',
        'maintenance_contract_start_date',
    ]
    
    

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        ordering = request.query_params.get('ordering', '-id')
        queryset = queryset.order_by(ordering)

        # Get the total count before pagination
        total_count = queryset.count()

        page = request.query_params.get('page')
        paginator = Paginator(queryset, 10)

        try:
            maintenancelifts = paginator.page(page)
        except PageNotAnInteger:
            maintenancelifts = paginator.page(1)
        except EmptyPage:
            maintenancelifts = paginator.page(paginator.num_pages)

        if page is None:
            page = 1

        page = int(page)
        
        serializer = MaintenanceLiftSerializer(maintenancelifts, many=True)

        # Include the total count in the JSON response
        response_data = {
            'MaintenanceLifts': serializer.data,
            'count': total_count,
            'page': page,
            'pages': paginator.num_pages
        }

        return JsonResponse(response_data)
           

    