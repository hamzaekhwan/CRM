
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *
from CRMapp.authentications.serializers import *
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]

    # filterset_fields = [
    #                     'isAdmin',
    #                    ]
    
    search_fields = ['username',
                     'email',
                     'first_name',
                     'last_name',]
    
    def get(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        
       
        data = {
            'count': count,
            'results': UserSerializer(queryset, many=True).data
        }

        return JsonResponse(data)
           