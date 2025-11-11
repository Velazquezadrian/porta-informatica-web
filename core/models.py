from django.db import models
from django.contrib.auth.models import User

# Modelo principal para cargar productos al catálogo
class Producto(models.Model):  # Modelo para productos
    # Opciones de categorías del menú (sincronizadas con menu_dinamico.js)
    CATEGORIA_CHOICES = [
        # Computadoras
        ('PC Armada', 'PC Armada'),
        
        # Notebook
        ('Lenovo', 'Lenovo'),
        ('Asus', 'Asus'),
        ('HP', 'HP'),
        ('Dell', 'Dell'),
        
        # Impresoras
        ('Laser', 'Laser'),
        ('Multifunción', 'Multifunción'),
        ('Matricial', 'Matricial'),
        
        # Almacenamiento
        ('SSD', 'SSD'),
        ('Disco Duro', 'Disco Duro'),
        ('Pendrive', 'Pendrive'),
        ('Tarjeta SD', 'Tarjeta SD'),
        ('Discos Externos', 'Discos Externos'),
        
        # Conectividad
        ('Router', 'Router'),
        ('Switch', 'Switch'),
        ('Extensores WiFi', 'Extensores WiFi'),
        ('USB WiFi', 'USB WiFi'),
        ('PCI WiFi', 'PCI WiFi'),
        
        # Componentes de PC
        ('Procesadores', 'Procesadores'),
        ('Motherboards', 'Motherboards'),
        ('Memorias RAM', 'Memorias RAM'),
        ('Placas de Video', 'Placas de Video'),
        ('Gabinetes', 'Gabinetes'),
        ('Fuentes', 'Fuentes'),
        ('Coolers', 'Coolers'),
        
        # Periféricos
        ('Mouse', 'Mouse'),
        ('Teclados', 'Teclados'),
        ('Auriculares', 'Auriculares'),
        ('Webcam', 'Webcam'),
        ('Parlantes', 'Parlantes'),
        ('Micrófonos', 'Micrófonos'),
        
        # Insumos
        ('Cartuchos', 'Cartuchos'),
        ('Tóners', 'Tóners'),
        ('Tintas', 'Tintas'),
        
        # Gaming
        ('Mouse Gamer', 'Mouse Gamer'),
        ('Teclados Gamer', 'Teclados Gamer'),
        ('Auriculares Gamer', 'Auriculares Gamer'),
        
        # Categorías principales (para "Ver todos")
        ('Computadoras', 'Computadoras'),
        ('Notebook', 'Notebook'),
        ('Impresoras', 'Impresoras'),
        ('Almacenamiento', 'Almacenamiento'),
        ('Conectividad', 'Conectividad'),
        ('Componentes de PC', 'Componentes de PC'),
        ('Periféricos', 'Periféricos'),
        ('Insumos', 'Insumos'),
        ('Gaming', 'Gaming'),
    ]
    
    nombre = models.CharField(max_length=100)  # Nombre del producto
    marca = models.CharField(max_length=50, blank=True, null=True, help_text='Marca del producto (ej: Logitech, HP, Samsung)')  # Marca opcional
    modelo = models.CharField(max_length=100, blank=True, null=True, help_text='Modelo o número de parte (ej: M170, ProBook 450)')
    descripcion = models.TextField()  # Descripción
    
    # Especificaciones técnicas detalladas
    caracteristicas = models.TextField(blank=True, null=True, help_text='Características principales (una por línea)')
    especificaciones_tecnicas = models.TextField(blank=True, null=True, help_text='Especificaciones técnicas detalladas (ej: procesador, RAM, etc.)')
    
    # Información de conectividad y energía
    conectividad = models.CharField(max_length=100, blank=True, null=True, help_text='Tipo de conexión (ej: Wireless 2.4GHz, Bluetooth, USB)')
    alimentacion = models.CharField(max_length=100, blank=True, null=True, help_text='Tipo de alimentación (ej: 1 pila AA, batería recargable, cable USB)')
    
    # Información de garantía y compatibilidad
    garantia = models.CharField(max_length=100, blank=True, null=True, help_text='Tiempo de garantía (ej: 12 meses, 2 años)')
    compatibilidad = models.TextField(blank=True, null=True, help_text='Sistemas operativos o dispositivos compatibles')
    
    # Campos básicos existentes
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio
    stock = models.IntegerField()  # Stock disponible
    imagen = models.ImageField(upload_to='productos/')  # Imagen
    activo = models.BooleanField(default=True)  # Mostrar/ocultar en catálogo
    categoria = models.CharField(
        max_length=100, 
        choices=CATEGORIA_CHOICES,
        help_text='Selecciona la categoría del menú donde aparecerá este producto'
    )  # Categoría obligatoria con opciones del menú

    def __str__(self):
        return self.nombre  # Muestra nombre en admin

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con User
    telefono = models.CharField(max_length=20, blank=True, null=True)  # Teléfono del usuario
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Dirección del usuario

    def __str__(self):
        return f"Perfil de {self.user.username}"  # Muestra el nombre de usuario


class Pedido(models.Model):
    """Pedido persistido (fase inicial – shadow write desde localStorage).
    Campos mínimos para reconstruir el pedido enviado por WhatsApp.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    nombre_cliente = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    mensaje_whatsapp = models.TextField(blank=True)  # Copia del mensaje generado (trazabilidad)

    def __str__(self):
        return f"Pedido #{self.id} - {self.creado:%Y-%m-%d %H:%M}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=150)  # Nombre congelado (por si cambia luego el producto)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} x{self.cantidad}"

    class Meta:
        verbose_name = 'Ítem de pedido'
        verbose_name_plural = 'Ítems de pedido'