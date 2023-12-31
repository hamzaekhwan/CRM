

from . import views


from django.urls import include, path


urlpatterns = [
path('contract-list/', views.ContractListView.as_view(),
         name='search_contract'),

path('contract-phase-list/', views.ContractPhaseListView.as_view(),
         name='search_contract_phase'),         

path('contract-list-maintenance/', views.ContractMaintenanceListView.as_view(),
         name='search_contract_has_a_maintenance'),

]
