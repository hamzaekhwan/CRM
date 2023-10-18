"""CRMsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


filter_urls = ['maintenances', 'contracts', 'clients', 'users']

urlpatterns = [
    path('admin/', admin.site.urls),
    path('CRMapp/authentications/', include('CRMapp.authentications.urls')),
    path('CRMapp/clients/', include('CRMapp.clients.urls')),
    path('CRMapp/contracts/', include('CRMapp.contracts.urls')),
    path('CRMapp/maintenances/', include('CRMapp.maintenances.urls')),
    path('CRMapp/maintenanceslift/', include('CRMapp.maintenanceslift.urls')),
    
    
    path('CRMapp/filters/maintenances/', include('CRMapp.filters.maintenances.urls')),
    path('CRMapp/filters/conracts/', include('CRMapp.filters.contracts.urls')),
    path('CRMapp/filters/clients/', include('CRMapp.filters.clients.urls')),
    path('CRMapp/filters/users/', include('CRMapp.filters.users.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
