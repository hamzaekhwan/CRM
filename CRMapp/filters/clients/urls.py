

from . import views


from django.urls import include, path


urlpatterns = [
path('client-list', views.ClientListView.as_view(),
         name='search_client'),

path('interest-list', views.InterestListView.as_view(),
         name='search_interest'),         
                 
]
