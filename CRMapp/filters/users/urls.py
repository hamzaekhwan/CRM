

from . import views


from django.urls import include, path


urlpatterns = [
path('list', views.UserListView.as_view(),
         name='search'),

         
                 
]
