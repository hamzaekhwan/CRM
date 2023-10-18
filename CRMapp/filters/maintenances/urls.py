

from . import views


from django.urls import include, path


urlpatterns = [
path('list', views.MaintenanceListView.as_view(),
         name='search'),

         
                 
]
