
from . import views


from django.urls import include, path

urlpatterns = [
    path('contract/', views.contract, name='contract'),    
    path('contract/<str:pk>/', views.contract, name='contract_by_id'),    # /<str:pk>/ for interest id
    path('getcontracts/', views.getcontracts, name='getcontracts pagination'), 

    path('contract_phases_by_id/<str:pk>/', views.contract_phases_by_id, name='contract_phases_by_id'), 
    path('maintenancelift_contract_by_id/<str:pk>/', views.maintenancelift_contract_by_id, name='contract_maintenances_by_id'), 
    path('maintenance_contract_by_id/<str:pk>/', views.maintenance_contract_by_id, name='maintenance_contract_by_id'), 
    path('note_contract_by_id/<str:pk>/', views.note_contract_by_id, name='note_contract_by_id'), 
    path('client_info_by_contract_by_id/<str:pk>/', views.client_info_by_contract_by_id, name='client_info_by_contract_by_id'), 
    
    path('distinct-floors/', views.DistinctFloorAPIView.as_view(), name='distinct-floors'),
    path('distinct-lift_type/', views.DistinctLiftTypeAPIView.as_view(), name='distinct-lift_type'),

    path('client/<str:pk>/', views.client, name='contract by id client'),   

    path('note/', views.note, name='note'),    
    path('note/<str:pk>/', views.note, name='note_by_id'),    
    path('getnotes/', views.getnotes, name='getnotes pagination'), 

    path('export-data-to-excel/', views.export_data_to_excel, name='export_data_to_excel'),




    path('phase/', views.phase, name='phase'),    
    path('phase/<str:pk>/', views.phase, name='phase_by_id'),  
    path('getphases/', views.getphases, name='getphases pagination'), 

    path('end_phase/<str:pk>/', views.end_phase, name='end_phase'),   
    



]