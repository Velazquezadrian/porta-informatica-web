from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public.urls')),# Sitio público
    path('panel/', include('core.urls')),# Panel interno   
    path('accounts/', include('django.contrib.auth.urls')), # URLs de autenticación
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), # Cerrar sesión
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
