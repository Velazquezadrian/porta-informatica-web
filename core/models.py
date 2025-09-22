from django.db import models
from django.contrib.auth.models import User

# Modelo principal para cargar productos al catálogo
class Producto(models.Model):  # Modelo para productos
    nombre = models.CharField(max_length=100)  # Nombre del producto
    descripcion = models.TextField()  # Descripción
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio
    stock = models.IntegerField()  # Stock disponible
    imagen = models.ImageField(upload_to='productos/')  # Imagen
    activo = models.BooleanField(default=True)  # Mostrar/ocultar en catálogo
    categoria = models.CharField(max_length=100, blank=True, null=True)  # Categoría opcional

    def __str__(self):
        return self.nombre  # Muestra nombre en admin

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con User
    telefono = models.CharField(max_length=20, blank=True, null=True)  # Teléfono del usuario
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Dirección del usuario

    def __str__(self):
        return f"Perfil de {self.user.username}"  # Muestra el nombre de usuario