
from . import views


from django.urls import include, path

urlpatterns = [
    path('client/', views.client, name='client'),    
    path('client/<str:pk>/', views.client, name='client_by_id'),   
     path('getclients/', views.getclients, name='getclients'),


    path('interest/', views.interest, name='interest'),  
    path('interest/<str:pk>/', views.interest, name='create-interest'),
    path('getinterests/', views.getinterests, name='getinterests'),
    path('distinct-cities/', views.DistinctCityAPIView.as_view(), name='distinct-cities'),
    

    path('reminder/', views.reminder, name='reminder'),  
    path('reminder/<str:pk>/', views.reminder, name='create-reminder'),
    # path('export/<str:file_type>/', views.export_file, name='export_file'),
]