

from . import views


from django.urls import include, path


urlpatterns = [
path('list', views.ElevatorContracListView.as_view(),
         name='search'),

         
                 
]
