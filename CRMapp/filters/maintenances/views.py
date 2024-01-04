
from rest_framework import generics
from CRMapp.models import *
from CRMapp.maintenances.serializers import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from CRMapp.authentications.permissions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class MaintenanceListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint]
    queryset = Maintenance.objects.all().order_by('-id')
    serializer_class = MaintenanceSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['type_name',
                        "contract__interest__client__city",
                        "contract__interest__company_name",
                        "contract__floors",
                        "contract__lift_type",
                        'contract__signed',]

    search_fields = ['contract__interest__client__name',
                     'contract__interest__client__arabic_name',
                     'contract__interest__client__city',
                     'contract__interest__client__mobile_phone',
                     'contract__ats',
                     'date']
    
    ordering_fields = [
        'type_name',
        'contract__interest__client__city',
        'contract__interest__company_name',
        'contract__floors',
        'contract__lift_type',
        'date',
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
            maintenances = paginator.page(page)
        except PageNotAnInteger:
            maintenances = paginator.page(1)
        except EmptyPage:
            maintenances = paginator.page(paginator.num_pages)

        if page is None:
            page = 1

        page = int(page)
        
        serializer = MaintenanceSerializer(maintenances, many=True)

        # Include the total count in the JSON response
        response_data = {
            'maintenances': serializer.data,
            'count': total_count,
            'page': page,
            'pages': paginator.num_pages
        }

        return JsonResponse(response_data)