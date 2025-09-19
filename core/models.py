from django.db import models

# Modelo principal para cargar productos al catálogo
class Producto(models.Model):  # Modelo para productos
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre # Muestra nombre en admin
