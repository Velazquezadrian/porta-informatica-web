from django.urls import path
from . import views
urlpatterns = [
    path('admin/subir/', views.subir_producto, name='subir_producto'),
    path('admin/lista/', views.lista_productos, name='lista_productos'),
]
