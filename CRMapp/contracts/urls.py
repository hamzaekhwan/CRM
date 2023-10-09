
from . import views


from django.urls import include, path

urlpatterns = [
    path('contract/', views.contract, name='contract'),    
    path('contract/<str:pk>/', views.contract, name='contract_by_id'),    
    path('contract_phases_by_id/<str:pk>/', views.contract_phases_by_id, name='contract_phases_by_id'),    

    path('note/', views.note, name='note'),    
    path('note/<str:pk>/', views.note, name='note_by_id'),    

    path('phase/', views.phase, name='phase'),    
    path('phase/<str:pk>/', views.phase, name='phase_by_id'),  
    path('end_phase/<str:pk>/', views.end_phase, name='end_phase'),   
    



]