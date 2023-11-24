from . import views


from django.urls import include, path

urlpatterns = [
    path('maintenance/', views.maintenance, name='maintenance'),    
    path('maintenance/<str:pk>/', views.maintenance, name='specific_maintenance'),
    path('login/', views.login_mobile, name='maintenance'),        ]