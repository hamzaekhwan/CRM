from . import views


from django.urls import include, path

urlpatterns = [
    path('maintenance/', views.maintenance_website, name='maintenance'),    
    path('maintenance/<str:pk>/', views.maintenance_website, name='specific_maintenance'),
  
    path('maintenance_mob/<str:pk>/', views.maintenance_mobile, name='specific_maintenance'),
    path('login/', views.login_mobile, name='maintenance'),]