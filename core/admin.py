from django.contrib import admin
from .models import Producto # Importamos el modelo Producto

# Registramos el modelo para que aparezca en el admin
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'activo') # Campos a mostrar en la lista
    search_fields = ('nombre', 'descripcion') # Campos para buscar
    list_filter = ('activo',) # Filtros laterales por categoría
