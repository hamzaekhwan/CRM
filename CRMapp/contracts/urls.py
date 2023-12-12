
from . import views


from django.urls import include, path

urlpatterns = [
    path('contract/', views.contract, name='contract'),    
    path('contract/<str:pk>/', views.contract, name='contract_by_id'),    # /<str:pk>/ for interest id
    path('get_contracts/', views.getcontracts, name='getcontracts pagination'), 

    path('contract_phases_by_id/<str:pk>/', views.contract_phases_by_id, name='contract_phases_by_id'), 
    path('maintenancelift_contract_by_id/<str:pk>/', views.maintenancelift_contract_by_id, name='contract_maintenances_by_id'), 
    path('maintenance_contract_by_id/<str:pk>/', views.maintenance_contract_by_id, name='maintenance_contract_by_id'), 

    path('client/<str:pk>/', views.client, name='contract by id client'),   

    path('note/', views.note, name='note'),    
    path('note/<str:pk>/', views.note, name='note_by_id'),    
    path('get_notes/', views.getnotes, name='getnotes pagination'), 



    path('phase/', views.phase, name='phase'),    
    path('phase/<str:pk>/', views.phase, name='phase_by_id'),  
    path('get_phases/', views.getphases, name='getphases pagination'), 

    path('end_phase/<str:pk>/', views.end_phase, name='end_phase'),   
    



]