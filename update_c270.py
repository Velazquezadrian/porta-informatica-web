#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portaside.settings')
django.setup()

from core.models import Producto

# Buscar producto Logitech C270
producto = Producto.objects.filter(nombre__icontains='c270').first()

if producto:
    # Actualizar campos con información real de la Logitech C270
    producto.marca = 'Logitech'
    producto.modelo = 'C270'
    
    producto.descripcion = '''Webcam HD con video de 720p y micrófono integrado. Ideal para videollamadas, streaming y grabación de contenido. Diseño compacto y fácil instalación plug-and-play.'''
    
    producto.caracteristicas = '''- Video HD 720p a 30 fps
- Micrófono integrado con reducción de ruido
- Enfoque automático
- Corrección automática de luz
- Clip universal ajustable
- Compatible con múltiples aplicaciones de videoconferencia
- Plug and Play - Sin instalación de software'''
    
    producto.especificaciones_tecnicas = '''Resolución de video: 1280 x 720 píxeles (720p HD)
Fotogramas por segundo: 30 fps
Tipo de enfoque: Enfoque fijo
Campo de visión: 60 grados
Longitud de cable: 1.5 metros
Interfaz: USB 2.0
Micrófono: Mono integrado
Dimensiones: 70 x 70 x 60 mm
Peso aproximado: 75g'''
    
    producto.conectividad = 'USB 2.0 (plug and play)'
    producto.alimentacion = 'Alimentación por USB (no requiere fuente externa)'
    producto.garantia = '2 años de garantía oficial Logitech'
    
    producto.compatibilidad = '''Windows 7, 8, 10, 11
macOS 10.10 o superior
Chrome OS
Compatible con:
- Skype
- Zoom
- Microsoft Teams
- Google Meet
- Discord
- OBS Studio
- Streamlabs'''
    
    producto.save()
    
    print(f'✓ Producto actualizado exitosamente:')
    print(f'  ID: {producto.id}')
    print(f'  Nombre: {producto.nombre}')
    print(f'  Marca: {producto.marca}')
    print(f'  Modelo: {producto.modelo}')
    print(f'  Campos actualizados: descripción, características, especificaciones, conectividad, alimentación, garantía, compatibilidad')
else:
    print('✗ No se encontró el producto Logitech C270')
