
from . import views


from django.urls import include, path

urlpatterns = [
    path('maintenancelift/', views.maintenancelift, name='maintenancelift'),    
    path('maintenancelift/<str:pk>/', views.maintenancelift, name='maintenancelift'),    
    path('getmaintenancelifts/', views.getmaintenancelifts, name='getmaintenancelifts pagination'), 






]