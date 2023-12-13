
from rest_framework import generics
from CRMapp.models import *
from CRMapp.maintenances.serializers import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from CRMapp.authentications.permissions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class MaintenanceListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint ]
    maintenances = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = ['type_name']
    
    search_fields = ['contract__interest__client__name',
                     'contract__interest__client__arabic_name',
                     'contract__interest__client__city',
                     'date']
 
    
    def get(self, request, *args, **kwargs):

        page = request.query_params.get('page')
        paginator = Paginator(self.maintenances, 10)

        try:
            maintenances = paginator.page(page)
        except PageNotAnInteger:
            maintenances = paginator.page(1)
        except EmptyPage:
            maintenances = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        
        serializer = MaintenanceSerializer(maintenances, many=True)
        return JsonResponse({'maintenances': serializer.data, 'page': page, 'pages': paginator.num_pages})