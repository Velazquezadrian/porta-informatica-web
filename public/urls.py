from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('pedido/', views.pedido, name='pedido'), # Página del carrito
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'), # Detalle del producto
    path('perfil/', views.perfil, name='perfil'), # Página de perfil del usuario
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), # Cerrar sesión
]