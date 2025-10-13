from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('registro/', views.registro, name='registro'),
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('pedido/', views.pedido, name='pedido'),
    path('pedido/confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
    path('producto/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
]
