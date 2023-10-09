
from . import views


from django.urls import include, path

urlpatterns = [
    path('client/', views.client, name='client'),    
    path('client/<str:pk>/', views.client, name='client_by_id'),    

]