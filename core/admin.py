from django.contrib import admin
from .models import Producto, Pedido, PedidoItem  # Importamos modelos

# Registramos el modelo para que aparezca en el admin
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'categoria', 'precio', 'stock', 'activo') # Campos a mostrar en la lista
    search_fields = ('nombre', 'descripcion', 'marca') # Campos para buscar
    list_filter = ('categoria', 'marca', 'activo',) # Filtros laterales por categoría, marca y estado


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ('nombre', 'cantidad', 'precio_unitario', 'subtotal')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'creado', 'nombre_cliente', 'telefono', 'metodo_pago', 'total')
    date_hierarchy = 'creado'
    search_fields = ('nombre_cliente', 'telefono', 'direccion')
    inlines = [PedidoItemInline]
    readonly_fields = ('creado', 'total', 'mensaje_whatsapp')
    fieldsets = (
        (None, {'fields': ('creado', 'user', 'nombre_cliente', 'telefono', 'direccion', 'metodo_pago', 'total')}),
        ('Mensaje generado', {'classes': ('collapse',), 'fields': ('mensaje_whatsapp',)}),
    )
