
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from CRMapp.authentications.permissions import *

class ContractListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint | IsEmp ]
    queryset = Contract.objects.all().order_by('-id')
    serializer_class = ContractSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = [
                        'lift_type',
                        'floors',
                        'interest__company_name',
                        'interest__client__city',
                        'signed',]
    
    search_fields = ['interest__client__name',
                     'interest__client__mobile_phone',
                     'interest__client__arabic_name',
                     'interest__client__city',
                     'interest__company_name',
                     'ats',
                     'location',
                     ]
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = request.query_params.get('page')
        paginator = Paginator(queryset, 10)

        try:
            contracts = paginator.page(page)
        except PageNotAnInteger:
            contracts = paginator.page(1)
        except EmptyPage:
            contracts = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        
        serializer = ContractSerializer(contracts, many=True)
        return JsonResponse({'contracts': serializer.data, 'page': page, 'pages': paginator.num_pages})
           


###for mobile search
class ContractMaintenanceListView(generics.ListAPIView):
    permission_classes = [ApiKeyPermission]
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['interest__client__name',
                     'interest__client__mobile_phone',
                     'interest__client__arabic_name',
                     'interest__client__city',
                     'interest__company_name',
                     'ats',
                     'location',]

    def get_queryset(self):
        # Only include contracts that have a corresponding MaintenanceLift
        queryset = Contract.objects.filter(maintenancelift__isnull=False).distinct()

        # Apply filters, search, and ordering
        queryset = self.filter_queryset(queryset)

        return queryset

    def get(self, request, *args, **kwargs):
        search_query = self.request.query_params.get('search', None)

        if search_query is None or search_query.strip() == '':
            # Return an empty array if the search query is empty
            data = {'count': 0, 'results': []}
        else:
            # Proceed with regular search and filtering logic
            queryset = self.get_queryset()
            count = queryset.count()

            data = {
                'count': count,
                'results': ContractSerializer(queryset, many=True).data
            }

        return JsonResponse(data, safe=False)


class ContractPhaseListView(generics.ListAPIView):    
    permission_classes = [IsManager | IsManagerMaint | IsEmp ]
    queryset = Phase.objects.all().order_by('-id')
    serializer_class = PhaseSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = [
                        'contract__lift_type',
                        'contract__floors',
                        'contract__signed',
                        'contract__interest__company_name',
                        'contract__interest__client__city',
                        'Name',]
    
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

        page = request.query_params.get('page')
        paginator = Paginator(queryset, 10)

        try:
            phases = paginator.page(page)
        except PageNotAnInteger:
            phases = paginator.page(1)
        except EmptyPage:
            phases = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        
        serializer = PhaseSerializer(phases, many=True)
        return JsonResponse({'phases': serializer.data, 'page': page, 'pages': paginator.num_pages})
           