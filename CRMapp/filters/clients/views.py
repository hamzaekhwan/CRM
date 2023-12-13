
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *
from CRMapp.clients.serializers import *
from CRMapp.authentications.permissions import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ClientListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint | IsEmp]
    clients = Client.objects.all()
    serializer_class = ClientSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = ['city']
 
    search_fields = ['name',
                     'arabic_name',
                     'city',
                     'mobile_phone',
                     ]

    def get(self, request, *args, **kwargs):

        page = request.query_params.get('page')
        paginator = Paginator(self.clients, 10)

        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            clients = paginator.page(1)
        except EmptyPage:
            clients = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        
        serializer = ClientSerializer(clients, many=True)
        return JsonResponse({'clients': serializer.data, 'page': page, 'pages': paginator.num_pages})
           

class InterestListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint | IsEmp]
    interests = Interest.objects.all()
    serializer_class = InterestSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    filterset_fields = ['client__city','inquiry','company_name']
    
    search_fields = ['client__name',
                     'client__arabic_name',
                     'client__city',
                     'client__mobile_phone',
                     'company_name'
                     ]
    
    def get(self, request, *args, **kwargs):

        page = request.query_params.get('page')
        paginator = Paginator(self.interests, 10)

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