#!/usr/bin/env python
"""
Script para importar productos masivamente desde C:\Redes porta
- Lee imágenes de subcarpetas organizadas
- Crea/actualiza productos con información técnica
- Copia imágenes al media folder
"""
import os
import django
import shutil
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portaside.settings')
django.setup()

from core.models import Producto

# Directorio base
BASE_DIR = Path(r"C:\Redes porta\Whatsapp")
MEDIA_DIR = Path(r"C:\Users\Usuario\portaside\media\productos")

# Información de productos conocidos
PRODUCTOS_INFO = {
    # Mouse Wireless Logitech
    "m170": {
        "nombre": "Mouse Logitech M170 Wireless",
        "marca": "Logitech",
        "modelo": "M170",
        "precio": 12500,
        "categoria": "Mouse",
        "descripcion": "Mouse inalámbrico compacto con conexión USB. Diseño ambidiestro y batería de larga duración.",
        "caracteristicas": """- Conexión inalámbrica 2.4 GHz
- Alcance inalámbrico de 10 metros
- Sensor óptico preciso
- Diseño ambidiestro
- Batería de hasta 12 meses
- Plug and play
- Rueda de desplazamiento suave""",
        "especificaciones_tecnicas": """Resolución: 1000 DPI
Tipo de sensor: Óptico
Botones: 3 botones (izquierdo, derecho, rueda)
Dimensiones: 99 x 60 x 38.4 mm
Peso: 78g (sin batería)
Cable receptor: Receptor nano USB
Color: Negro""",
        "conectividad": "Wireless 2.4 GHz con receptor nano USB",
        "alimentacion": "1 pila AA (incluida)",
        "garantia": "2 años de garantía Logitech",
        "compatibilidad": "Windows 7/8/10/11, macOS 10.5 o superior, Chrome OS, Linux kernel 2.6+"
    },
    "m185": {
        "nombre": "Mouse Logitech M185 Wireless",
        "marca": "Logitech",
        "modelo": "M185",
        "precio": 14000,
        "categoria": "Mouse",
        "descripcion": "Mouse inalámbrico confiable con conexión plug-and-play. Diseño ergonómico cómodo para uso diario.",
        "caracteristicas": """- Conexión inalámbrica 2.4 GHz
- Alcance de 10 metros
- Sensor óptico avanzado
- Diseño ergonómico
- Batería de hasta 12 meses
- Receptor nano USB compacto
- Compatible con múltiples sistemas operativos""",
        "especificaciones_tecnicas": """Resolución: 1000 DPI
Tipo de sensor: Óptico avanzado
Botones: 3 botones
Dimensiones: 99 x 60 x 39 mm
Peso: 75.2g (sin batería)
Interfaz: USB mediante receptor inalámbrico
Colores disponibles: Negro, Gris""",
        "conectividad": "Wireless 2.4 GHz con receptor nano USB",
        "alimentacion": "1 pila AA",
        "garantia": "2 años oficial Logitech",
        "compatibilidad": "Windows XP/Vista/7/8/10/11, macOS 10.5+, Chrome OS, Linux 2.6+"
    },
    "m187": {
        "nombre": "Mouse Logitech M187 Ultra Portable Wireless",
        "marca": "Logitech",
        "modelo": "M187",
        "precio": 15500,
        "categoria": "Mouse",
        "descripcion": "Mouse ultra portátil y compacto. Perfecto para notebooks y tablets. Diseño minimalista de alta calidad.",
        "caracteristicas": """- Diseño ultra compacto
- Conexión inalámbrica confiable
- Sensor óptico preciso
- Clic silencioso
- Batería de larga duración
- Fácil guardado del receptor
- Ideal para viajes""",
        "especificaciones_tecnicas": """Resolución: 1000 DPI
Tipo de sensor: Óptico
Botones: 3 botones
Dimensiones: 84 x 49 x 33 mm
Peso: 57g (con batería)
Receptor: Nano USB almacenable
Color: Negro, Blanco, Rojo""",
        "conectividad": "Wireless 2.4 GHz",
        "alimentacion": "1 pila AA (hasta 12 meses)",
        "garantia": "2 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, macOS, Chrome OS, Linux"
    },
    "m190": {
        "nombre": "Mouse Logitech M190 Full-Size Wireless",
        "marca": "Logitech",
        "modelo": "M190",
        "precio": 16000,
        "categoria": "Mouse",
        "descripcion": "Mouse inalámbrico de tamaño completo con diseño ergonómico contorneado. Comodidad durante todo el día.",
        "caracteristicas": """- Diseño de tamaño completo
- Forma contorneada ergonómica
- Conexión inalámbrica confiable 2.4 GHz
- Alcance de 10 metros
- Batería de 18 meses
- Rueda de desplazamiento precisa
- Plug and play""",
        "especificaciones_tecnicas": """Resolución: 1000 DPI
Sensor: Óptico
Botones: 3 botones estándar
Dimensiones: 105.4 x 67.9 x 38.9 mm
Peso: 91g (con batería)
Receptor: Nano USB
Colores: Gris, Azul, Rojo, Amarillo""",
        "conectividad": "Wireless 2.4 GHz con receptor nano",
        "alimentacion": "1 pila AA (duración 18 meses)",
        "garantia": "2 años garantía oficial",
        "compatibilidad": "Windows 10/11, macOS 10.15+, Chrome OS, Linux"
    },
    "m196": {
        "nombre": "Mouse Logitech M196 Bluetooth",
        "marca": "Logitech",
        "modelo": "M196",
        "precio": 18000,
        "categoria": "Mouse",
        "descripcion": "Mouse Bluetooth silencioso con tecnología SilentTouch. Reducción de ruido del 90% en los clics.",
        "caracteristicas": """- Tecnología Bluetooth
- Clics silenciosos (SilentTouch)
- Reducción de ruido del 90%
- Sensor óptico de precisión
- Diseño ergonómico
- Batería de larga duración
- Sin receptor USB necesario""",
        "especificaciones_tecnicas": """Resolución: 1000 DPI
Tipo de sensor: Óptico de alta precisión
Botones: 3 botones silenciosos
Dimensiones: 99 x 60 x 38 mm
Peso: 78g
Conectividad: Bluetooth Low Energy
Alcance: 10 metros""",
        "conectividad": "Bluetooth 5.0",
        "alimentacion": "1 pila AA (hasta 18 meses)",
        "garantia": "2 años Logitech",
        "compatibilidad": "Windows 8/10/11, macOS 10.10+, Chrome OS, Android 5.0+, iPadOS 13.4+"
    },
    "m240": {
        "nombre": "Mouse Logitech M240 Silent Bluetooth",
        "marca": "Logitech",
        "modelo": "M240",
        "precio": 20000,
        "categoria": "Mouse",
        "descripcion": "Mouse Bluetooth ultra silencioso y portátil. Conectividad Bluetooth sin receptor, ideal para trabajar sin molestar.",
        "caracteristicas": """- Tecnología SilentTouch
- 90% más silencioso
- Conexión Bluetooth sin receptor
- Diseño compacto y portátil
- Sensor óptico preciso
- Batería hasta 18 meses
- Compatible con múltiples dispositivos""",
        "especificaciones_tecnicas": """Resolución: 1000 DPI
Sensor: Óptico avanzado
Botones: 3 botones ultra silenciosos
Dimensiones: 99.1 x 60.5 x 38.5 mm
Peso: 79g (con batería)
Tecnología: Bluetooth Low Energy
Alcance: 10 metros""",
        "conectividad": "Bluetooth LE",
        "alimentacion": "1 pila AA (18 meses)",
        "garantia": "2 años oficial Logitech",
        "compatibilidad": "Windows 10/11, macOS 10.15+, Chrome OS, Linux, iPadOS 13.4+, Android 5.0+"
    },
    "m280": {
        "nombre": "Mouse Logitech M280 Wireless",
        "marca": "Logitech",
        "modelo": "M280",
        "precio": 17500,
        "categoria": "Mouse",
        "descripcion": "Mouse inalámbrico con diseño ergonómico contorneado y rueda de goma suave. Comodidad excepcional.",
        "caracteristicas": """- Diseño ergonómico contorneado
- Rueda de goma suave
- Conexión inalámbrica confiable
- Sensor óptico preciso
- Batería de 18 meses
- Receptor nano USB compacto
- Forma que se adapta a la mano""",
        "especificaciones_tecnicas": """Resolución: 1000 DPI
Tipo de sensor: Óptico avanzado
Botones: 3 botones
Dimensiones: 105.4 x 67.9 x 38.9 mm
Peso: 91.2g (con batería)
Receptor: USB nano
Colores: Negro, Azul, Rojo""",
        "conectividad": "Wireless 2.4 GHz",
        "alimentacion": "1 pila AA (duración 18 meses)",
        "garantia": "2 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, macOS 10.5+, Chrome OS, Linux"
    },
    "8300s": {
        "nombre": "Mouse Inalámbrico 8300S",
        "marca": "Generic",
        "modelo": "8300S",
        "precio": 8500,
        "categoria": "Mouse",
        "descripcion": "Mouse inalámbrico económico con diseño ergonómico. Ideal para uso diario en oficina o hogar.",
        "caracteristicas": """- Conexión inalámbrica 2.4 GHz
- Diseño ergonómico básico
- Sensor óptico
- 3 botones estándar
- Alcance de hasta 10m
- Plug and play
- Ahorro de energía automático""",
        "especificaciones_tecnicas": """Resolución: 1000 DPI
Sensor: Óptico
Botones: 3 botones
Alcance: 10 metros
Dimensiones: 100 x 65 x 40 mm
Peso: 85g""",
        "conectividad": "Wireless 2.4 GHz con receptor USB",
        "alimentacion": "2 pilas AAA",
        "garantia": "6 meses",
        "compatibilidad": "Windows XP/7/8/10/11, macOS, Linux"
    },
    "10850": {
        "nombre": "Mouse Inalámbrico 10850",
        "marca": "Generic",
        "modelo": "10850",
        "precio": 7500,
        "categoria": "Mouse",
        "descripcion": "Mouse inalámbrico básico para uso general. Buena relación precio-calidad.",
        "caracteristicas": """- Conexión inalámbrica
- Sensor óptico básico
- 3 botones
- Diseño estándar
- Bajo consumo de energía
- Fácil instalación""",
        "especificaciones_tecnicas": """Resolución: 800 DPI
Sensor: Óptico
Botones: 3
Alcance: 8 metros
Peso: 75g""",
        "conectividad": "Wireless 2.4 GHz",
        "alimentacion": "2 pilas AAA",
        "garantia": "3 meses",
        "compatibilidad": "Windows, macOS, Linux"
    },
    # Webcams
    "c270": {
        "nombre": "Webcam Logitech C270 HD",
        "marca": "Logitech",
        "modelo": "C270",
        "precio": 35000,
        "categoria": "Webcam",
        "descripcion": "Webcam HD con video de 720p y micrófono integrado. Ideal para videollamadas, streaming y grabación de contenido.",
        "caracteristicas": """- Video HD 720p a 30 fps
- Micrófono integrado con reducción de ruido
- Enfoque automático
- Corrección automática de luz
- Clip universal ajustable
- Compatible con múltiples aplicaciones de videoconferencia
- Plug and Play - Sin instalación de software""",
        "especificaciones_tecnicas": """Resolución de video: 1280 x 720 píxeles (720p HD)
Fotogramas por segundo: 30 fps
Tipo de enfoque: Enfoque fijo
Campo de visión: 60 grados
Longitud de cable: 1.5 metros
Interfaz: USB 2.0
Micrófono: Mono integrado
Dimensiones: 70 x 70 x 60 mm
Peso aproximado: 75g""",
        "conectividad": "USB 2.0 (plug and play)",
        "alimentacion": "Alimentación por USB (no requiere fuente externa)",
        "garantia": "2 años de garantía oficial Logitech",
        "compatibilidad": """Windows 7/8/10/11, macOS 10.10+, Chrome OS
Compatible con: Skype, Zoom, Microsoft Teams, Google Meet, Discord, OBS Studio, Streamlabs"""
    },
    "facecam2000x2": {
        "nombre": "Webcam Elgato Facecam 2000X2",
        "marca": "Elgato",
        "modelo": "Facecam 2000X2",
        "precio": 95000,
        "categoria": "Webcam",
        "descripcion": "Webcam profesional 4K para streaming y creación de contenido. Calidad de imagen excepcional.",
        "caracteristicas": """- Resolución 4K a 60 fps
- Sensor Sony STARVIS CMOS
- Campo de visión ajustable
- Micrófono integrado de alta calidad
- Montaje universal
- Software de control avanzado
- Enfoque automático rápido""",
        "especificaciones_tecnicas": """Resolución: 3840 x 2160 (4K UHD)
FPS: 60 fps en 4K, 120 fps en 1080p
Sensor: Sony STARVIS CMOS
Campo de visión: 82 grados (ajustable)
Interfaz: USB 3.0 Type-C
Longitud de cable: 2 metros
Dimensiones: 60 x 60 x 80 mm""",
        "conectividad": "USB 3.0 Type-C",
        "alimentacion": "Alimentación por USB",
        "garantia": "2 años Elgato",
        "compatibilidad": "Windows 10/11 (64-bit), macOS 11+, OBS, Streamlabs, XSplit"
    },
    "hw80s": {
        "nombre": "Webcam HD HW80S HDC",
        "marca": "Generic",
        "modelo": "HW80S HDC",
        "precio": 18000,
        "categoria": "Webcam",
        "descripcion": "Webcam HD económica con micrófono integrado. Buena opción para videollamadas básicas.",
        "caracteristicas": """- Video HD 720p
- Micrófono integrado
- Enfoque manual
- Clip ajustable
- Plug and play
- Compatible con aplicaciones de videoconferencia
- Bajo costo""",
        "especificaciones_tecnicas": """Resolución: 1280 x 720 (720p)
FPS: 30 fps
Campo de visión: 70 grados
Interfaz: USB 2.0
Cable: 1.5 metros
Micrófono: Integrado
Peso: 100g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "6 meses",
        "compatibilidad": "Windows 7/8/10/11, macOS, aplicaciones de videoconferencia estándar"
    },
    
    # === TECLADOS GAMING ===
    "k215": {
        "nombre": "Teclado Gamer K215",
        "marca": "Generic",
        "modelo": "K215",
        "precio": 15000,
        "categoria": "Teclados Gamer",
        "descripcion": "Teclado gaming con retroiluminación LED y teclas de respuesta rápida.",
        "caracteristicas": """- Retroiluminación LED RGB
- Teclas de membrana
- Anti-ghosting
- Diseño ergonómico
- Teclas multimedia
- Cable USB reforzado
- Resistente a salpicaduras""",
        "especificaciones_tecnicas": """Tipo: Membrana gaming
Teclas: 104 teclas
Retroiluminación: LED RGB
Interfaz: USB 2.0
Cable: 1.5m trenzado
Dimensiones: 440 x 130 x 30 mm
Peso: 650g""",
        "conectividad": "USB 2.0 cable",
        "alimentacion": "USB (no requiere alimentación externa)",
        "garantia": "6 meses",
        "compatibilidad": "Windows XP/7/8/10/11, macOS, Linux, PS4"
    },
    "kg901": {
        "nombre": "Teclado Gamer KG901",
        "marca": "Generic",
        "modelo": "KG901",
        "precio": 18000,
        "categoria": "Teclados Gamer",
        "descripcion": "Teclado mecánico gaming con switches blue y retroiluminación LED multicolor.",
        "caracteristicas": """- Switches mecánicos Blue
- Retroiluminación LED multicolor
- Anti-ghosting completo
- Teclas de acceso rápido
- Reposamanos desmontable
- Construcción robusta
- Modo gaming (bloqueo tecla Windows)""",
        "especificaciones_tecnicas": """Tipo: Mecánico Blue switches
Teclas: 104 teclas + multimedia
Retroiluminación: LED multicolor
Vida útil switches: 50 millones de pulsaciones
Cable: USB 1.8m trenzado
Dimensiones: 445 x 135 x 35 mm
Peso: 850g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "1 año",
        "compatibilidad": "Windows 7/8/10/11, macOS 10.5+, Linux"
    },
    "mage": {
        "nombre": "Teclado Gamer Mage",
        "marca": "Redragon",
        "modelo": "Mage K570",
        "precio": 22000,
        "categoria": "Teclados Gamer",
        "descripcion": "Teclado mecánico gaming RGB con switches Outemu Blue. Diseño premium con efectos de iluminación personalizables.",
        "caracteristicas": """- Switches mecánicos Outemu Blue
- Retroiluminación RGB personalizable
- 104 teclas anti-ghosting
- Teclas multimedia dedicadas
- Construcción en aluminio
- Reposamanos magnético
- 12 modos de iluminación""",
        "especificaciones_tecnicas": """Tipo: Mecánico Outemu Blue
Teclas: 104 teclas
Retroiluminación: RGB programable
Vida útil: 60 millones de pulsaciones
Polling rate: 1000Hz
Cable: 1.8m trenzado antigolpes
Material: Marco de aluminio
Peso: 1.1kg""",
        "conectividad": "USB 2.0 gold-plated",
        "alimentacion": "USB",
        "garantia": "2 años Redragon",
        "compatibilidad": "Windows XP/7/8/10/11, macOS, Linux, PS4, Xbox One"
    },
    "smk5900sb3": {
        "nombre": "Teclado Gamer SMK-5900SB-3",
        "marca": "Sentey",
        "modelo": "SMK-5900SB-3",
        "precio": 19500,
        "categoria": "Teclados Gamer",
        "descripcion": "Teclado semi-mecánico gaming con retroiluminación RGB y respuesta táctil mejorada.",
        "caracteristicas": """- Switches semi-mecánicos
- Retroiluminación RGB 7 colores
- 19 teclas anti-ghosting
- Teclas multimedia
- Diseño compacto
- Apoyamanos ergonómico
- Resistente a líquidos""",
        "especificaciones_tecnicas": """Tipo: Semi-mecánico
Teclas: 104 teclas
Retroiluminación: RGB 7 colores
Interfaz: USB 2.0
Cable: 1.5m
Dimensiones: 440 x 125 x 28 mm
Peso: 700g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "1 año",
        "compatibilidad": "Windows 7/8/10/11"
    },
    "xtk531s": {
        "nombre": "Teclado Gamer XTK-531S",
        "marca": "Xtrike Me",
        "modelo": "XTK-531S",
        "precio": 16500,
        "categoria": "Teclados Gamer",
        "descripcion": "Teclado gaming con iluminación LED y teclas flotantes de alta respuesta.",
        "caracteristicas": """- Teclas flotantes
- Retroiluminación LED
- 26 teclas anti-ghosting
- Teclas multimedia integradas
- Diseño ergonómico
- Cable USB trenzado
- Plug and play""",
        "especificaciones_tecnicas": """Tipo: Membrana gaming
Teclas: 105 teclas
Retroiluminación: LED single color
Interfaz: USB
Cable: 1.5m trenzado
Dimensiones: 445 x 160 x 30 mm
Peso: 600g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "6 meses",
        "compatibilidad": "Windows 7/8/10/11, macOS, PS4"
    },
    "z12": {
        "nombre": "Teclado Gamer Zealot Z12",
        "marca": "Zealot",
        "modelo": "Z12",
        "precio": 14000,
        "categoria": "Teclados Gamer",
        "descripcion": "Teclado gaming económico con retroiluminación LED y teclas de respuesta rápida.",
        "caracteristicas": """- Retroiluminación LED
- Teclas de respuesta rápida
- Anti-ghosting
- Diseño ergonómico
- Teclas multimedia
- Resistente a salpicaduras
- Bajo costo""",
        "especificaciones_tecnicas": """Tipo: Membrana
Teclas: 104 teclas
Retroiluminación: LED single color
Interfaz: USB 2.0
Cable: 1.3m
Peso: 550g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 meses",
        "compatibilidad": "Windows XP/7/8/10/11"
    },
    
    # === TECLADOS OFICINA ===
    "8101": {
        "nombre": "Teclado USB 8101",
        "marca": "Generic",
        "modelo": "8101",
        "precio": 4500,
        "categoria": "Teclados",
        "descripcion": "Teclado básico USB para uso general en oficina. Económico y funcional.",
        "caracteristicas": """- Teclas de membrana
- Diseño estándar
- Plug and play
- Silencioso
- Resistente
- Bajo consumo
- Teclas estables""",
        "especificaciones_tecnicas": """Tipo: Membrana
Teclas: 104 teclas
Interfaz: USB 2.0
Cable: 1.4m
Dimensiones: 440 x 130 x 25 mm
Peso: 450g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 meses",
        "compatibilidad": "Windows, macOS, Linux"
    },
    "820": {
        "nombre": "Teclado USB 820",
        "marca": "Generic",
        "modelo": "820",
        "precio": 5000,
        "categoria": "Teclados",
        "descripcion": "Teclado USB estándar con diseño ergonómico básico.",
        "caracteristicas": """- Teclas de membrana suaves
- Diseño estándar
- Teclas silenciosas
- Plug and play
- Resistente al uso diario
- Patas ajustables""",
        "especificaciones_tecnicas": """Tipo: Membrana
Teclas: 104 teclas
Interfaz: USB
Cable: 1.5m
Peso: 480g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 meses",
        "compatibilidad": "Universal"
    },
    "k120": {
        "nombre": "Teclado Logitech K120",
        "marca": "Logitech",
        "modelo": "K120",
        "precio": 12000,
        "categoria": "Teclados",
        "descripcion": "Teclado USB básico de Logitech. Confiable, cómodo y resistente a derrames.",
        "caracteristicas": """- Teclas de perfil bajo
- Resistente a líquidos
- Teclas silenciosas
- Patas ajustables
- Diseño fino
- Plug and play
- Teclas curvas cómodas""",
        "especificaciones_tecnicas": """Tipo: Membrana
Teclas: 104 teclas
Interfaz: USB 2.0
Cable: 1.5m
Dimensiones: 450 x 155 x 23.5 mm
Peso: 550g
Resistencia: Hasta 10 millones de pulsaciones""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, Linux kernel 2.6+"
    },
    "k270": {
        "nombre": "Teclado Logitech K270 Wireless",
        "marca": "Logitech",
        "modelo": "K270",
        "precio": 18000,
        "categoria": "Teclados",
        "descripcion": "Teclado inalámbrico Logitech con teclas de tamaño completo y batería de larga duración.",
        "caracteristicas": """- Conexión inalámbrica 2.4 GHz
- Alcance de 10 metros
- Batería hasta 24 meses
- Teclas de tamaño completo
- 8 teclas de acceso rápido
- Resistente a salpicaduras
- Receptor nano USB""",
        "especificaciones_tecnicas": """Tipo: Membrana wireless
Teclas: 104 teclas + 8 teclas rápidas
Interfaz: USB wireless 2.4 GHz
Alcance: 10 metros
Dimensiones: 441.5 x 149 x 18 mm
Peso: 470g (sin pilas)
Duración batería: 24 meses""",
        "conectividad": "Wireless 2.4 GHz",
        "alimentacion": "2 pilas AAA",
        "garantia": "3 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, Chrome OS"
    },
    "kb117": {
        "nombre": "Teclado KB-117",
        "marca": "Generic",
        "modelo": "KB-117",
        "precio": 6000,
        "categoria": "Teclados",
        "descripcion": "Teclado USB económico con diseño estándar.",
        "caracteristicas": """- Teclas de membrana
- Diseño estándar
- Plug and play
- Teclas estables
- Resistente
- Patas ajustables""",
        "especificaciones_tecnicas": """Tipo: Membrana
Teclas: 104 teclas
Interfaz: USB
Cable: 1.4m
Peso: 460g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 meses",
        "compatibilidad": "Windows, Linux"
    },
    "kb117s": {
        "nombre": "Teclado KB-117S",
        "marca": "Generic",
        "modelo": "KB-117S",
        "precio": 6500,
        "categoria": "Teclados",
        "descripcion": "Teclado USB silencioso con teclas suaves al tacto.",
        "caracteristicas": """- Teclas silenciosas
- Membrana suave
- Plug and play
- Diseño compacto
- Patas ajustables
- Resistente""",
        "especificaciones_tecnicas": """Tipo: Membrana silenciosa
Teclas: 104 teclas
Interfaz: USB
Cable: 1.4m
Peso: 450g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 meses",
        "compatibilidad": "Universal"
    },
    "luxemate110": {
        "nombre": "Teclado Luxemate 110",
        "marca": "Luxemate",
        "modelo": "110",
        "precio": 7500,
        "categoria": "Teclados",
        "descripcion": "Teclado USB con diseño ergonómico y teclas confortables.",
        "caracteristicas": """- Diseño ergonómico
- Teclas confortables
- Silencioso
- Resistente a salpicaduras
- Patas ajustables
- Plug and play""",
        "especificaciones_tecnicas": """Tipo: Membrana
Teclas: 104 teclas
Interfaz: USB 2.0
Cable: 1.5m
Dimensiones: 445 x 135 x 25 mm
Peso: 520g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "6 meses",
        "compatibilidad": "Windows, macOS, Linux"
    },
    "mk220": {
        "nombre": "Combo Logitech MK220 Wireless",
        "marca": "Logitech",
        "modelo": "MK220",
        "precio": 22000,
        "categoria": "Teclados",
        "descripcion": "Combo inalámbrico Logitech con teclado y mouse compactos. Ideal para espacios reducidos.",
        "caracteristicas": """- Teclado y mouse incluidos
- Conexión inalámbrica
- Receptor único nano USB
- Teclado compacto
- Mouse óptico
- Batería de larga duración
- Plug and play""",
        "especificaciones_tecnicas": """Teclado: 84 teclas
Mouse: 1000 DPI óptico
Interfaz: USB wireless 2.4 GHz
Alcance: 10 metros
Batería teclado: 24 meses (2 AAA)
Batería mouse: 5 meses (1 AA)
Dimensiones teclado: 299 x 130 x 18 mm""",
        "conectividad": "Wireless 2.4 GHz compartido",
        "alimentacion": "Teclado 2 AAA, Mouse 1 AA",
        "garantia": "2 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, Chrome OS"
    },
    "mk235": {
        "nombre": "Combo Logitech MK235 Wireless",
        "marca": "Logitech",
        "modelo": "MK235",
        "precio": 25000,
        "categoria": "Teclados",
        "descripcion": "Combo inalámbrico con teclado tamaño completo y mouse óptico. Batería de larga duración.",
        "caracteristicas": """- Teclado de tamaño completo
- Mouse óptico incluido
- Receptor USB único
- Batería hasta 36 meses (teclado)
- Resistente a salpicaduras
- 8 teclas de acceso rápido
- Diseño ergonómico""",
        "especificaciones_tecnicas": """Teclado: 104 teclas + 8 teclas rápidas
Mouse: 1000 DPI
Interfaz: Wireless 2.4 GHz
Alcance: 10 metros
Batería: Teclado 36 meses, Mouse 12 meses
Dimensiones teclado: 450 x 155 x 22 mm""",
        "conectividad": "Wireless 2.4 GHz",
        "alimentacion": "Teclado 2 AAA, Mouse 1 AA",
        "garantia": "3 años Logitech",
        "compatibilidad": "Windows 7/8/10/11"
    },
    "mk270": {
        "nombre": "Combo Logitech MK270 Wireless",
        "marca": "Logitech",
        "modelo": "MK270",
        "precio": 26500,
        "categoria": "Teclados",
        "descripcion": "Combo inalámbrico confiable con teclado tamaño completo y mouse ergonómico.",
        "caracteristicas": """- Teclado inalámbrico completo
- Mouse ergonómico óptico
- Receptor nano USB único
- Batería hasta 24 meses
- 8 teclas de acceso rápido
- Resistente a líquidos
- Plug and play""",
        "especificaciones_tecnicas": """Teclado: 104 teclas + multimedia
Mouse: 1000 DPI óptico
Interfaz: Wireless 2.4 GHz
Alcance: 10 metros
Batería teclado: 24 meses (2 AAA)
Batería mouse: 12 meses (1 AA)""",
        "conectividad": "Wireless 2.4 GHz",
        "alimentacion": "Pilas AAA y AA",
        "garantia": "3 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, Chrome OS"
    },
    "mk295": {
        "nombre": "Combo Logitech MK295 Silent Wireless",
        "marca": "Logitech",
        "modelo": "MK295",
        "precio": 28000,
        "categoria": "Teclados",
        "descripcion": "Combo inalámbrico silencioso con tecnología SilentTouch. Reduce el ruido hasta 90%.",
        "caracteristicas": """- Tecnología SilentTouch
- 90% más silencioso
- Teclado y mouse incluidos
- Batería hasta 36 meses
- Resistente a salpicaduras
- Teclas de acceso rápido
- Receptor nano único""",
        "especificaciones_tecnicas": """Teclado: 104 teclas silenciosas
Mouse: 1000 DPI silencioso
Interfaz: Wireless 2.4 GHz
Alcance: 10 metros
Batería teclado: 36 meses
Batería mouse: 18 meses
Dimensiones: 441.5 x 149 x 18 mm""",
        "conectividad": "Wireless 2.4 GHz",
        "alimentacion": "2 AAA (teclado), 1 AA (mouse)",
        "garantia": "3 años Logitech",
        "compatibilidad": "Windows 10/11, macOS 10.15+, Chrome OS"
    },
    "mk345": {
        "nombre": "Combo Logitech MK345 Wireless",
        "marca": "Logitech",
        "modelo": "MK345",
        "precio": 29000,
        "categoria": "Teclados",
        "descripcion": "Combo inalámbrico premium con teclado ergonómico y reposamanos acolchado.",
        "caracteristicas": """- Teclado ergonómico
- Reposamanos acolchado
- Mouse contorneado
- 12 teclas programables
- Batería hasta 36 meses
- Resistente a salpicaduras
- Receptor Unifying""",
        "especificaciones_tecnicas": """Teclado: 104 teclas + 12 programables
Mouse: 1000 DPI ergonómico
Interfaz: Logitech Unifying
Alcance: 10 metros
Batería: 36 meses (teclado), 18 meses (mouse)
Dimensiones: 456 x 193 x 23 mm""",
        "conectividad": "Wireless Unifying 2.4 GHz",
        "alimentacion": "2 AAA (teclado), 1 AA (mouse)",
        "garantia": "3 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, Chrome OS"
    },
    
    # === PARLANTES ===
    "hf520bt": {
        "nombre": "Parlantes Bluetooth HF520BT",
        "marca": "Havit",
        "modelo": "HF520BT",
        "precio": 24000,
        "categoria": "Parlantes",
        "descripcion": "Parlantes Bluetooth 5.0 con sonido estéreo de alta calidad. Conexión inalámbrica y cable auxiliar.",
        "caracteristicas": """- Bluetooth 5.0
- Sonido estéreo 2.0
- Entrada auxiliar 3.5mm
- Control de volumen integrado
- Alimentación USB
- LED indicador
- Diseño compacto""",
        "especificaciones_tecnicas": """Potencia: 6W (3W x 2)
Bluetooth: 5.0
Alcance: 10 metros
Respuesta de frecuencia: 80Hz - 18KHz
S/N: ≥80dB
Impedancia: 4Ω
Entrada: USB 5V / AUX 3.5mm
Dimensiones: 80 x 80 x 90 mm cada uno""",
        "conectividad": "Bluetooth 5.0, AUX 3.5mm",
        "alimentacion": "USB 5V",
        "garantia": "1 año",
        "compatibilidad": "Dispositivos con Bluetooth, smartphones, tablets, PC, notebooks"
    },
    "q180": {
        "nombre": "Parlantes Genius Q180",
        "marca": "Genius",
        "modelo": "Q180",
        "precio": 12000,
        "categoria": "Parlantes",
        "descripcion": "Parlantes USB 2.0 compactos con sonido claro. Ideal para PC y notebooks.",
        "caracteristicas": """- Sonido estéreo 2.0
- Conexión USB
- Control de volumen frontal
- Diseño compacto
- Plug and play
- LED indicador de encendido
- Base antideslizante""",
        "especificaciones_tecnicas": """Potencia: 4W (2W x 2)
Interfaz: USB 2.0
Respuesta de frecuencia: 100Hz - 17KHz
S/N: ≥75dB
Impedancia: 4Ω
Cable: 1.2m
Dimensiones: 65 x 75 x 75 mm cada uno
Peso: 300g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB (no requiere fuente externa)",
        "garantia": "1 año",
        "compatibilidad": "Windows XP/7/8/10/11, macOS, Linux"
    },
    "soundbar100": {
        "nombre": "Soundbar Dell AC411",
        "marca": "Dell",
        "modelo": "Soundbar 100",
        "precio": 35000,
        "categoria": "Parlantes",
        "descripcion": "Soundbar profesional para monitor con sonido estéreo de alta calidad. Montaje universal.",
        "caracteristicas": """- Montaje para monitor
- Sonido estéreo potente
- Conexión USB
- Control de volumen touch
- LED indicador
- Diseño delgado
- Base ajustable universal""",
        "especificaciones_tecnicas": """Potencia: 10W (5W x 2)
Interfaz: USB 2.0
Respuesta de frecuencia: 90Hz - 20KHz
S/N: ≥85dB
Drivers: 2 x 1.6 pulgadas
Cable: 1.8m
Dimensiones: 410 x 65 x 65 mm
Peso: 450g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB powered",
        "garantia": "1 año Dell",
        "compatibilidad": "Windows 7/8/10/11, macOS, monitores con base estándar"
    },
    "sw21300": {
        "nombre": "Parlantes Genius SW-2.1 300",
        "marca": "Genius",
        "modelo": "SW-2.1 300",
        "precio": 28000,
        "categoria": "Parlantes",
        "descripcion": "Sistema de parlantes 2.1 con subwoofer de madera. Sonido potente para PC y entretenimiento.",
        "caracteristicas": """- Sistema 2.1 con subwoofer
- Subwoofer de madera
- Control de volumen y bajos
- Entrada auxiliar 3.5mm
- LED indicador
- Satélites blindados
- Sonido potente""",
        "especificaciones_tecnicas": """Potencia total: 12W RMS
Subwoofer: 6W
Satélites: 3W x 2
Respuesta de frecuencia: 40Hz - 20KHz
S/N: ≥80dB
Impedancia: 4Ω
Entrada: 3.5mm stereo
Cable satélites: 1.2m
Dimensiones subwoofer: 150 x 180 x 150 mm""",
        "conectividad": "Cable 3.5mm stereo",
        "alimentacion": "220V AC",
        "garantia": "1 año",
        "compatibilidad": "PC, notebooks, smartphones, tablets, reproductores MP3"
    },
    
    # === AURICULARES OFICINA ===
    "h111": {
        "nombre": "Auricular Logitech H111 Stereo",
        "marca": "Logitech",
        "modelo": "H111",
        "precio": 16000,
        "categoria": "Auriculares",
        "descripcion": "Auricular estéreo con micrófono giratorio. Ideal para videollamadas y uso diario.",
        "caracteristicas": """- Sonido estéreo
- Micrófono giratorio con reducción de ruido
- Controles de volumen integrados
- Almohadillas acolchadas
- Cable de 2.4m
- Jack 3.5mm doble
- Diadema ajustable""",
        "especificaciones_tecnicas": """Drivers: 30mm
Respuesta de frecuencia: 20Hz - 20KHz
Impedancia: 32Ω
Sensibilidad: 100dB
Micrófono: Omnidireccional
Frecuencia mic: 100Hz - 16KHz
Conexión: Doble jack 3.5mm
Cable: 2.4m
Peso: 100g""",
        "conectividad": "Jack 3.5mm (auricular y micrófono separados)",
        "alimentacion": "No requiere",
        "garantia": "2 años Logitech",
        "compatibilidad": "PC, notebooks con entradas separadas de audio y micrófono"
    },
    "hs02b": {
        "nombre": "Auricular USB HS-02B",
        "marca": "Generic",
        "modelo": "HS-02B",
        "precio": 8500,
        "categoria": "Auriculares",
        "descripcion": "Auricular USB básico para call center y oficina. Económico y funcional.",
        "caracteristicas": """- Conexión USB
- Micrófono flexible
- Control de volumen en cable
- Almohadillas suaves
- Diadema ajustable
- Plug and play
- Liviano""",
        "especificaciones_tecnicas": """Drivers: 30mm
Impedancia: 32Ω
Sensibilidad: 95dB
Micrófono: Flexible omnidireccional
Conexión: USB 2.0
Cable: 1.8m
Peso: 90g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 meses",
        "compatibilidad": "Windows XP/7/8/10/11, macOS, Linux"
    },
    "hs230u": {
        "nombre": "Auricular Genius HS-230U USB",
        "marca": "Genius",
        "modelo": "HS-230U",
        "precio": 11000,
        "categoria": "Auriculares",
        "descripcion": "Auricular USB con micrófono ajustable y almohadillas cómodas. Para uso prolongado.",
        "caracteristicas": """- Conexión USB plug and play
- Micrófono ajustable
- Almohadillas acolchadas
- Control de volumen
- Diadema ajustable
- Cable reforzado
- Sonido claro""",
        "especificaciones_tecnicas": """Drivers: 30mm neodimio
Respuesta: 20Hz - 20KHz
Impedancia: 32Ω
Sensibilidad: 100dB
Micrófono: -58dB ±3dB
Conexión: USB 2.0
Cable: 2m
Peso: 110g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "1 año",
        "compatibilidad": "Windows XP/7/8/10/11, macOS 10.5+, Linux"
    },
    
    # === AURICULARES GRANDES (Celular/Música) ===
    "4105": {
        "nombre": "Auriculares Noblex HP4105",
        "marca": "Noblex",
        "modelo": "HP4105",
        "precio": 15000,
        "categoria": "Auriculares",
        "descripcion": "Auriculares over-ear con sonido de alta calidad. Almohadillas acolchadas para uso prolongado.",
        "caracteristicas": """- Diseño over-ear
- Almohadillas acolchadas
- Cable desmontable
- Diadema ajustable
- Sonido balanceado
- Plegables
- Jack 3.5mm""",
        "especificaciones_tecnicas": """Drivers: 40mm
Respuesta: 20Hz - 20KHz
Impedancia: 32Ω
Sensibilidad: 105dB
Conexión: Jack 3.5mm
Cable: 1.2m desmontable
Peso: 180g""",
        "conectividad": "Jack 3.5mm",
        "alimentacion": "No requiere",
        "garantia": "1 año",
        "compatibilidad": "Smartphones, tablets, notebooks, reproductores MP3"
    },
    "mt120": {
        "nombre": "Auriculares MT120",
        "marca": "Generic",
        "modelo": "MT120",
        "precio": 9000,
        "categoria": "Auriculares",
        "descripcion": "Auriculares estéreo básicos con micrófono integrado. Económicos y versátiles.",
        "caracteristicas": """- Diseño on-ear
- Micrófono integrado
- Control de llamadas
- Almohadillas suaves
- Cable plano anti-enredos
- Plegables
- Colores disponibles""",
        "especificaciones_tecnicas": """Drivers: 30mm
Impedancia: 32Ω
Sensibilidad: 98dB
Micrófono: MEMS integrado
Conexión: Jack 3.5mm
Cable: 1.2m
Peso: 130g""",
        "conectividad": "Jack 3.5mm con control de llamadas",
        "alimentacion": "No requiere",
        "garantia": "6 meses",
        "compatibilidad": "Smartphones, tablets, notebooks"
    },
    "tune525": {
        "nombre": "Auriculares JBL Tune 525BT",
        "marca": "JBL",
        "modelo": "Tune 525BT",
        "precio": 42000,
        "categoria": "Auriculares",
        "descripcion": "Auriculares Bluetooth con JBL Pure Bass Sound. Batería de larga duración y diseño plegable.",
        "caracteristicas": """- Bluetooth 5.0
- JBL Pure Bass Sound
- Batería hasta 50 horas
- Carga rápida (5 min = 3 horas)
- Micrófono integrado
- Plegables
- Multipoint connection
- Control táctil""",
        "especificaciones_tecnicas": """Drivers: 32mm dinámicos
Respuesta: 20Hz - 20KHz
Bluetooth: 5.0
Alcance: 10 metros
Batería: 50 horas
Carga: USB-C
Tiempo carga completa: 2 horas
Peso: 160g""",
        "conectividad": "Bluetooth 5.0, cable auxiliar 3.5mm incluido",
        "alimentacion": "Batería recargable USB-C",
        "garantia": "1 año JBL",
        "compatibilidad": "Smartphones, tablets, notebooks con Bluetooth"
    },
    
    # === AURICULARES GAMING ===
    "ds501": {
        "nombre": "Auriculares Gamer DS501",
        "marca": "Generic",
        "modelo": "DS501",
        "precio": 18000,
        "categoria": "Auriculares Gamer",
        "descripcion": "Auriculares gaming con iluminación LED RGB y sonido surround 7.1. Micrófono flexible.",
        "caracteristicas": """- Iluminación LED RGB
- Sonido surround 7.1 virtual
- Micrófono flexible con reducción de ruido
- Almohadillas de cuero sintético
- Control de volumen en cable
- Drivers de 50mm
- Diseño ergonómico""",
        "especificaciones_tecnicas": """Drivers: 50mm neodimio
Respuesta: 20Hz - 20KHz
Impedancia: 32Ω ±15%
Sensibilidad: 110dB ±3dB
Micrófono: -42dB ±3dB
Conexión: USB 2.0
Cable: 2.2m trenzado
Peso: 320g
Iluminación: LED RGB""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "6 meses",
        "compatibilidad": "Windows 7/8/10/11, PS4, PS5"
    },
    "g335": {
        "nombre": "Auriculares Logitech G335 Gaming",
        "marca": "Logitech",
        "modelo": "G335",
        "precio": 48000,
        "categoria": "Auriculares Gamer",
        "descripcion": "Auriculares gaming ligeros con sonido inmersivo. Micrófono con flip-to-mute y diseño ultra cómodo.",
        "caracteristicas": """- Ultra ligeros (240g)
- Drivers 40mm
- Micrófono flip-to-mute
- Almohadillas de tela transpirable
- Suspensión de diadema
- Cable de 2m
- Controles en cable
- Colores disponibles""",
        "especificaciones_tecnicas": """Drivers: 40mm neodimio
Respuesta: 20Hz - 20KHz
Impedancia: 36Ω
Sensibilidad: 87.5dB
Micrófono: 6mm cardioide
Frecuencia mic: 100Hz - 10KHz
Conexión: Jack 3.5mm
Cable: 2m
Peso: 240g""",
        "conectividad": "Jack 3.5mm (compatible con adaptador Y para PC)",
        "alimentacion": "No requiere",
        "garantia": "2 años Logitech",
        "compatibilidad": "PC, PS4, PS5, Xbox One, Xbox Series X/S, Nintendo Switch, móviles"
    },
    "gh331": {
        "nombre": "Auriculares Mars Gaming GH331",
        "marca": "Mars Gaming",
        "modelo": "GH331",
        "precio": 22000,
        "categoria": "Auriculares Gamer",
        "descripcion": "Auriculares gaming con iluminación LED dual y sonido potente. Diseño ergonómico.",
        "caracteristicas": """- Iluminación LED dual
- Drivers de 50mm
- Micrófono omnidireccional flexible
- Almohadillas de memoria
- Diadema autoajustable
- Control de volumen
- Cable trenzado
- Multi-plataforma""",
        "especificaciones_tecnicas": """Drivers: 50mm neodimio
Respuesta: 20Hz - 20KHz
Impedancia: 32Ω
Sensibilidad: 108dB
Micrófono: Omnidireccional
Conexión: Jack 3.5mm + USB (LED)
Cable: 2m trenzado
Peso: 310g""",
        "conectividad": "Jack 3.5mm + USB para LED",
        "alimentacion": "USB solo para LED",
        "garantia": "2 años",
        "compatibilidad": "PC, PS4, PS5, Xbox, Switch, móviles"
    },
    "hs05a": {
        "nombre": "Auriculares Gamer HS-05A",
        "marca": "Generic",
        "modelo": "HS-05A",
        "precio": 15000,
        "categoria": "Auriculares Gamer",
        "descripcion": "Auriculares gaming económicos con LED y micrófono. Buena relación precio-calidad.",
        "caracteristicas": """- Iluminación LED
- Micrófono flexible
- Almohadillas acolchadas
- Control de volumen
- Diadema ajustable
- Cable reforzado
- Sonido estéreo""",
        "especificaciones_tecnicas": """Drivers: 40mm
Respuesta: 20Hz - 20KHz
Impedancia: 32Ω
Sensibilidad: 105dB
Micrófono: -42dB
Conexión: USB + Jack 3.5mm
Cable: 2m
Peso: 280g""",
        "conectividad": "USB (LED) + Jack 3.5mm (audio)",
        "alimentacion": "USB para LED",
        "garantia": "3 meses",
        "compatibilidad": "PC, PS4, Xbox One"
    },
    
    # === JOYSTICKS ===
    "f310": {
        "nombre": "Gamepad Logitech F310",
        "marca": "Logitech",
        "modelo": "F310",
        "precio": 35000,
        "categoria": "Joystick",
        "descripcion": "Gamepad USB con diseño tipo consola. Compatible con una amplia gama de juegos.",
        "caracteristicas": """- Diseño ergonómico
- D-pad de 4 direcciones
- 2 sticks analógicos
- 10 botones programables
- Modo XInput y DirectInput
- Vibración de respuesta
- Cable USB 1.8m
- Plug and play""",
        "especificaciones_tecnicas": """Botones: 10 botones + 2 gatillos
Sticks: 2 analógicos
D-pad: 4 direcciones
Vibración: Sí
Interfaz: USB 2.0
Cable: 1.8m
Dimensiones: 160 x 110 x 65 mm
Peso: 280g""",
        "conectividad": "USB 2.0 cableado",
        "alimentacion": "USB (no requiere pilas)",
        "garantia": "2 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, Steam"
    },
    "f710": {
        "nombre": "Gamepad Logitech F710 Wireless",
        "marca": "Logitech",
        "modelo": "F710",
        "precio": 55000,
        "categoria": "Joystick",
        "descripcion": "Gamepad inalámbrico premium con vibración y sticks programables. Hasta 10 metros de alcance.",
        "caracteristicas": """- Conexión inalámbrica 2.4 GHz
- Alcance de 10 metros
- Vibración de respuesta
- 2 sticks analógicos
- D-pad de 8 direcciones
- Modo XInput y DirectInput
- Indicador LED de batería
- Diseño ergonómico""",
        "especificaciones_tecnicas": """Botones: 10 botones + 2 gatillos
Sticks: 2 analógicos programables
D-pad: 8 direcciones
Vibración: Dual motor
Interfaz: Wireless 2.4 GHz
Alcance: 10 metros
Batería: 2 pilas AA
Dimensiones: 156 x 106 x 62 mm
Peso: 350g (con pilas)""",
        "conectividad": "Wireless 2.4 GHz con receptor USB nano",
        "alimentacion": "2 pilas AA",
        "garantia": "2 años Logitech",
        "compatibilidad": "Windows 7/8/10/11, Steam, Android TV"
    },
    "gx17uv": {
        "nombre": "Gamepad GX-17UV",
        "marca": "Generic",
        "modelo": "GX-17UV",
        "precio": 15000,
        "categoria": "Joystick",
        "descripcion": "Gamepad USB económico con diseño clásico. Buena opción para gaming casual.",
        "caracteristicas": """- Diseño ergonómico
- 2 sticks analógicos
- 12 botones de acción
- D-pad
- Vibración
- Cable USB
- Plug and play
- Bajo costo""",
        "especificaciones_tecnicas": """Botones: 12 botones
Sticks: 2 analógicos
D-pad: 8 direcciones
Vibración: Sí
Interfaz: USB 2.0
Cable: 1.5m
Peso: 250g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 meses",
        "compatibilidad": "Windows XP/7/8/10/11"
    },
    "j7024": {
        "nombre": "Joystick J7024",
        "marca": "Generic",
        "modelo": "J7024",
        "precio": 12000,
        "categoria": "Joystick",
        "descripcion": "Joystick USB básico para PC. Económico y funcional.",
        "caracteristicas": """- Diseño simple
- 2 sticks analógicos
- 10 botones
- D-pad
- Cable USB
- Plug and play
- Económico""",
        "especificaciones_tecnicas": """Botones: 10 botones
Sticks: 2 analógicos
D-pad: Sí
Interfaz: USB
Cable: 1.3m
Peso: 230g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "3 meses",
        "compatibilidad": "Windows XP/7/8/10"
    },
    "nmp401": {
        "nombre": "Gamepad Netmak NM-P401",
        "marca": "Netmak",
        "modelo": "NM-P401",
        "precio": 18000,
        "categoria": "Joystick",
        "descripcion": "Gamepad con diseño tipo PlayStation. Vibración y sticks sensibles.",
        "caracteristicas": """- Diseño tipo PlayStation
- Vibración dual
- 2 sticks analógicos
- 12 botones
- D-pad de 8 direcciones
- Cable USB reforzado
- Goma antideslizante""",
        "especificaciones_tecnicas": """Botones: 12 botones
Sticks: 2 analógicos
D-pad: 8 direcciones
Vibración: Dual motor
Interfaz: USB 2.0
Cable: 1.8m
Peso: 270g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "6 meses",
        "compatibilidad": "Windows 7/8/10/11"
    },
    "nmxtreme": {
        "nombre": "Gamepad Netmak NM-Xtreme",
        "marca": "Netmak",
        "modelo": "NM-Xtreme",
        "precio": 20000,
        "categoria": "Joystick",
        "descripcion": "Gamepad gaming con iluminación LED y vibración. Diseño ergonómico premium.",
        "caracteristicas": """- Iluminación LED
- Vibración dual potente
- Sticks analógicos precisos
- 12 botones de acción
- Gatillos analógicos
- Cable USB trenzado
- Diseño ergonómico
- Agarre antideslizante""",
        "especificaciones_tecnicas": """Botones: 12 botones + gatillos
Sticks: 2 analógicos sensibles
D-pad: 8 direcciones
Vibración: Dual motor
LED: Iluminación integrada
Interfaz: USB 2.0
Cable: 2m trenzado
Peso: 300g""",
        "conectividad": "USB 2.0",
        "alimentacion": "USB",
        "garantia": "1 año",
        "compatibilidad": "Windows 7/8/10/11, PS3"
    },
}

def normalizar_nombre_archivo(filename):
    """Convierte nombre de archivo a key del diccionario"""
    # Quitar extensión y convertir a minúsculas
    base = os.path.splitext(filename)[0].lower()
    # Quitar espacios y caracteres especiales
    base = base.replace(" ", "").replace("-", "").replace("_", "")
    return base

def copiar_imagen(source_path, producto_key):
    """Copia imagen al directorio media"""
    if not os.path.exists(source_path):
        return None
    
    # Crear directorio si no existe
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Nombre de destino
    ext = os.path.splitext(source_path)[1]
    dest_filename = f"{producto_key}{ext}"
    dest_path = MEDIA_DIR / dest_filename
    
    # Copiar archivo
    shutil.copy2(source_path, dest_path)
    
    # Retornar path relativo para Django
    return f"productos/{dest_filename}"

def procesar_productos():
    """Procesa todos los productos y sus imágenes"""
    productos_creados = 0
    productos_actualizados = 0
    errores = []
    
    # Recorrer estructura de carpetas
    for root, dirs, files in os.walk(BASE_DIR):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Normalizar nombre para buscar en diccionario
                key = normalizar_nombre_archivo(filename)
                
                if key in PRODUCTOS_INFO:
                    info = PRODUCTOS_INFO[key]
                    filepath = os.path.join(root, filename)
                    
                    try:
                        # Copiar imagen
                        imagen_path = copiar_imagen(filepath, key)
                        
                        if not imagen_path:
                            errores.append(f"No se pudo copiar imagen: {filename}")
                            continue
                        
                        # Buscar o crear producto
                        producto, created = Producto.objects.get_or_create(
                            modelo=info['modelo'],
                            marca=info['marca'],
                            defaults={
                                'nombre': info['nombre'],
                                'precio': info['precio'],
                                'categoria': info['categoria'],
                                'descripcion': info['descripcion'],
                                'caracteristicas': info['caracteristicas'],
                                'especificaciones_tecnicas': info['especificaciones_tecnicas'],
                                'conectividad': info['conectividad'],
                                'alimentacion': info['alimentacion'],
                                'garantia': info['garantia'],
                                'compatibilidad': info['compatibilidad'],
                                'imagen': imagen_path,
                                'stock': 10,
                                'activo': True
                            }
                        )
                        
                        if created:
                            productos_creados += 1
                            print(f"✓ Creado: {info['nombre']}")
                        else:
                            # Actualizar producto existente
                            producto.nombre = info['nombre']
                            producto.precio = info['precio']
                            producto.categoria = info['categoria']
                            producto.descripcion = info['descripcion']
                            producto.caracteristicas = info['caracteristicas']
                            producto.especificaciones_tecnicas = info['especificaciones_tecnicas']
                            producto.conectividad = info['conectividad']
                            producto.alimentacion = info['alimentacion']
                            producto.garantia = info['garantia']
                            producto.compatibilidad = info['compatibilidad']
                            producto.imagen = imagen_path
                            if producto.stock == 0:
                                producto.stock = 10
                            producto.save()
                            productos_actualizados += 1
                            print(f"↻ Actualizado: {info['nombre']}")
                    
                    except Exception as e:
                        errores.append(f"Error con {filename}: {str(e)}")
                        print(f"✗ Error: {filename} - {str(e)}")
    
    # Resumen
    print("\n" + "="*60)
    print(f"Productos creados: {productos_creados}")
    print(f"Productos actualizados: {productos_actualizados}")
    if errores:
        print(f"\nErrores ({len(errores)}):")
        for error in errores:
            print(f"  - {error}")
    print("="*60)

if __name__ == "__main__":
    print("Iniciando importación de productos...")
    print(f"Directorio base: {BASE_DIR}")
    print(f"Directorio media: {MEDIA_DIR}\n")
    procesar_productos()
