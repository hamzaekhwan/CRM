

from . import views


from django.urls import include, path


urlpatterns = [
path('list', views.ContractListView.as_view(),
         name='search'),

         
                 
]
