

from . import views


from django.urls import include, path


urlpatterns = [
path('login', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

path('change-password', views.ChangePasswordView.as_view(), name='change-password'),   
path('admin/', views.admin, name='admin'),    
path('admin/<int:pk>/', views.admin, name='admin_by_id'),     
         
         
                 
]
