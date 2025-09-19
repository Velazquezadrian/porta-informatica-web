from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public.urls')),# Sitio público
    path('panel/', include('core.urls')),# Panel interno
]
