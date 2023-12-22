
from rest_framework import generics
from CRMapp.models import *
from CRMapp.contracts.serializers import *
from CRMapp.authentications.serializers import *
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from CRMapp.authentications.permissions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
class UserListView(generics.ListAPIView):
    permission_classes = [IsManager | IsManagerMaint ]
    queryset = User.objects.all().order_by('-id')
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

        page = request.query_params.get('page')
        paginator = Paginator(queryset, 10)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)
        
        serializer = UserSerializer(users, many=True)
        return JsonResponse({'users': serializer.data, 'page': page, 'pages': paginator.num_pages})
           