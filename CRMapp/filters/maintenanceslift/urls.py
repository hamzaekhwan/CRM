

from . import views


from django.urls import include, path


urlpatterns = [
path('list/', views.MaintenanceLiftListView.as_view(),
         name='search'),

         
                 
]
