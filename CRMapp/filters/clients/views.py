
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *
from CRMapp.clients.serializers import *
from CRMapp.authentications.permissions import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_filters import FilterSet, DateFromToRangeFilter

class ClientFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = Client
        fields =['city','date',]

class ClientListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint | IsEmp]
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ClientFilter

    # filterset_fields = ['city']
 
    search_fields = ['name', 'arabic_name', 'city', 'mobile_phone']
    
    ordering_fields = ['name', 'city', 'date']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
       
        ordering = request.query_params.get('ordering', '-id')
        queryset = queryset.order_by(ordering)

        # Get the total count before pagination
        total_count = queryset.count()
        
        page = request.query_params.get('page')
        paginator = Paginator(queryset, 10)

        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            clients = paginator.page(1)
        except EmptyPage:
            clients = paginator.page(paginator.num_pages)

        if page is None:
            page = 1

        page = int(page)
        
        serializer = ClientSerializer(clients, many=True)

        # Include the total count in the JSON response
        response_data = {
            'clients': serializer.data,
            'count': total_count,
            'page': page,
            'pages': paginator.num_pages
        }

        return JsonResponse(response_data)

    
           

class InterestListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint | IsEmp]
    queryset = Interest.objects.all().order_by('-id')
    serializer_class = InterestSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = ['client__city','company_name']
    
    search_fields = ['client__name',
                     'client__arabic_name',
                     'client__city',
                     'client__mobile_phone',
                     'company_name'
                     ]
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = request.query_params.get('page')
        paginator = Paginator(queryset, 10)

        try:
            interests = paginator.page(page)
        except PageNotAnInteger:
            interests = paginator.page(1)
        except EmptyPage:
            interests = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        
        serializer = InterestSerializer(interests, many=True)
        return JsonResponse({'interests': serializer.data, 'page': page, 'pages': paginator.num_pages})