

from . import views


from django.urls import include, path


urlpatterns = [
path('list', views.ClientListView.as_view(),
         name='search'),

         
                 
]
