Readme Técnico - porta-informatica-web

## Descripción General

Este proyecto es una aplicación web e-commerce desarrollada con Django 5.2.6, orientada a la gestión y venta de productos informáticos. El sistema cuenta con una sección administrativa completa y una tienda pública moderna con carrito de compras lateral, permitiendo la gestión integral de productos y una experiencia de compra fluida para los usuarios.

## Arquitectura del Sistema

### Separación de Apps
- **core/**: Gestión administrativa y modelos de datos
- **public/**: Catálogo público, carrito y experiencia del cliente

### Flujo de Datos del Carrito
1. **Cliente (localStorage)**: Los productos se agregan al carrito almacenado localmente en el navegador
2. **Sidebar Cart**: UI lateral que muestra items del carrito en tiempo real
3. **Confirmación**: Al completar compra, datos se envían al servidor para persistencia
4. **Servidor (Pedido/PedidoItem)**: Modelos Django que almacenan pedidos confirmados con validación de stock

## Estructura del Proyecto

### core/ - Administración y Modelos
- **models.py**: 
  - `Producto`: Modelo principal (nombre, descripcion, precio, stock, imagen, activo, categoria, marca, etc)
  - `Perfil`: Extensión de User con teléfono y dirección
  - `Pedido`: Pedidos confirmados con datos del cliente y total
  - `PedidoItem`: Items individuales de cada pedido con precio congelado
- **admin.py**: Panel de administración Django customizado
- **forms.py**: Formularios para gestión de productos y perfiles
- **views.py**: Vistas administrativas (subir_producto, lista_productos)
- **urls.py**: Rutas administrativas
- **templates/admin/**: Plantillas para gestión interna

### public/ - Tienda Pública
- **views.py**: 
  - `home()`: Catálogo con filtros (categoría, búsqueda, precio) y paginación
  - `producto_detalle()`: Vista individual de producto
  - `pedido()`: Página de checkout/resumen
  - `confirmar_pedido()`: API para persistir pedidos (POST /pedido/confirmar/)
  - `buscar()`: Búsqueda avanzada con filtros de marca y precio
  - `categoria_detalle()`: Listado por categoría específica
- **urls.py**: Rutas públicas (home, buscar, producto, pedido, perfil, etc)
- **static/**:
  - `css/style.css`: Estilos completos con gradientes, animaciones, sidebar cart
  - `js/carrito.js`: Lógica del carrito (agregar, eliminar, sidebar, WhatsApp, persistencia)
  - `js/menu_dinamico.js`: Generación dinámica del menú de categorías
  - `img/`: Logos, iconos, carrusel
- **templates/public/**:
  - `base.html`: Template maestro con navbar, sidebar cart, footer, WhatsApp flotante
  - `home.html`: Página principal con carrusel de productos destacados
  - `producto_detalle.html`: Detalle completo del producto
  - `pedido.html`: Formulario de checkout con datos del cliente
  - `buscar.html`: Resultados de búsqueda con filtros laterales
  - `categoria.html`: Listado de productos por categoría
  - Otras: `contacto.html`, `servicios.html`, `perfil.html`, `editar_perfil.html`, `registro.html`
- **templatetags/custom_filters.py**: Filtros personalizados para templates
- **tests_pedido.py**: Tests unitarios para flujo de pedidos (mantener)

### Configuración Principal
- **portaside/settings.py**: 
  - Apps: core, public
  - TEMPLATES: DIRS apunta a public/templates, APP_DIRS=True para core
  - MEDIA_ROOT/MEDIA_URL: Configuración de archivos subidos
  - STATIC_ROOT/STATIC_URL: Assets estáticos
- **portaside/urls.py**: Routing principal incluyendo core.urls y public.urls
- **portaside/wsgi.py**: Configuración WSGI para deploy

### Otros Archivos
- **media/productos/**: Imágenes de productos subidas por admin
- **db.sqlite3**: Base de datos de desarrollo (46 productos)
- **requirements.txt**: Dependencias (Django 5.2.6, Pillow)
- **importar_productos.py**: Script para carga masiva de productos
- **env/**: Entorno virtual Python

## Funcionalidades Implementadas

### Administración
✅ CRUD completo de productos con imágenes
✅ Panel de administración Django con permisos
✅ Gestión de categorías y marcas
✅ Control de stock e inventario
✅ Sistema de perfiles de usuario

### Tienda Pública
✅ Catálogo con filtros (categoría, búsqueda, rango de precio)
✅ Paginación (12 productos por página)
✅ Carrusel de productos destacados aleatorios
✅ Sidebar cart deslizante con animaciones suaves
✅ Agregar/eliminar productos del carrito individual
✅ Contador de items en navbar
✅ Vista detalle de producto con specs completas
✅ Búsqueda avanzada por nombre, descripción, marca
✅ Navegación por categorías jerárquicas
✅ Página de checkout con formulario de cliente
✅ Envío de pedido por WhatsApp (wa.me)
✅ Persistencia de pedidos en servidor (shadow write)
✅ Validación de stock antes de confirmar
✅ Descuento automático de inventario
✅ Botón flotante de WhatsApp empresarial
✅ Diseño responsive mobile-first
✅ Gradientes y animaciones CSS modernas

### Sistema de Carrito (Arquitectura Híbrida)
**Fase 1 - Cliente (actual)**:
- localStorage para velocidad y UX offline
- Sidebar lateral para ver items sin cambiar página
- Contador en tiempo real
- Eliminación individual de productos

**Fase 2 - Servidor (sombra)**:
- `confirmar_pedido()` persiste en modelos Pedido/PedidoItem
- Validación de stock atómica (transaction.atomic)
- Precio congelado en momento de compra
- Trazabilidad completa de pedidos

## Tecnologías Utilizadas

### Backend
- **Python 3.13**
- **Django 5.2.6**
  - ORM para modelos
  - Sistema de templates
  - Admin customizado
  - Autenticación de usuarios
- **Pillow**: Procesamiento de imágenes
- **SQLite**: Base de datos (dev)

### Frontend
- **HTML5/CSS3**
  - Flexbox y Grid
  - Animaciones y transiciones
  - Custom properties (--color-primario)
- **JavaScript ES6+**
  - LocalStorage API
  - Fetch API para AJAX
  - Manipulación del DOM
- **Bootstrap 5** (parcial, principalmente CSS custom)
- **Bootstrap Icons** (SVG)

## Modelos de Datos

### Producto
```python
nombre: CharField(150)
descripcion: TextField
precio: DecimalField(10,2)
stock: PositiveIntegerField
imagen: ImageField(upload_to='productos/')
activo: BooleanField(default=True)
categoria: CharField(100, choices=CATEGORIA_CHOICES)
marca: CharField(100, blank=True)
modelo: CharField(100, blank=True)
caracteristicas: TextField(blank=True)
especificaciones_tecnicas: TextField(blank=True)
conectividad: CharField(255, blank=True)
alimentacion: CharField(255, blank=True)
garantia: CharField(255, blank=True)
compatibilidad: TextField(blank=True)
```

### Pedido
```python
user: ForeignKey(User, null=True)
creado: DateTimeField(auto_now_add=True)
nombre_cliente: CharField(150)
telefono: CharField(30)
direccion: CharField(255)
metodo_pago: CharField(50)
total: DecimalField(12,2)
mensaje_whatsapp: TextField
```

### PedidoItem
```python
pedido: ForeignKey(Pedido, related_name='items')
producto: ForeignKey(Producto, null=True)
nombre: CharField(150)  # congelado
cantidad: PositiveIntegerField
precio_unitario: DecimalField(10,2)  # congelado
subtotal: DecimalField(12,2)
```

## URLs Principales

### Públicas
- `/` - Home con catálogo
- `/buscar/?q=...` - Búsqueda avanzada
- `/c/<categoria>/<subcategoria>/` - Listado por categoría
- `/producto/<id>/` - Detalle de producto
- `/pedido/` - Página de checkout
- `/pedido/confirmar/` - API POST para persistir pedido
- `/contacto/` - Formulario de contacto
- `/servicios/` - Servicios de la empresa
- `/perfil/` - Perfil del usuario
- `/editar-perfil/` - Editar datos personales
- `/registro/` - Registro de nuevos usuarios
- `/login/` - Login (Django auth)

### Administrativas
- `/admin/` - Panel Django admin
- `/admin/core/producto/` - CRUD productos
- `/admin/core/pedido/` - Ver pedidos confirmados

## Sistema de Categorías

Categorías implementadas (sincronizadas con menu_dinamico.js):
- **Computadoras**: PC Armada
- **Notebook**: Lenovo, Asus, HP, Dell
- **Impresoras**: Laser, Multifunción, Matricial
- **Almacenamiento**: SSD, Disco Duro, Pendrive, Tarjeta SD, Discos Externos
- **Conectividad**: Router, Switch, Extensor Wifi, Adaptador Wifi
- **Accesorios de PC**: Fuente de Poder, Gabinete, Cooler/Ventilador
- **Periféricos**: Teclado, Mouse, Webcam, Parlante, Micrófono, Joystick
- **Gaming**: Mouse Gamer, Teclado Gamer, Auriculares Gamer, Silla Gamer
- **Monitores**: LCD, LED, Curvo, Gaming

## Comandos Esenciales

```bash
# Activar entorno virtual
env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Servidor de desarrollo
python manage.py runserver

# Cargar productos en masa
python importar_productos.py

# Ejecutar tests
python manage.py test public.tests_pedido
```

## Archivos Eliminados (Limpieza Nov 2025)

❌ **update_c270.py** - Script one-off para actualizar producto C270 (ya ejecutado)
❌ **corregir_categorias.py** - Script one-off para corregir categorías de joysticks/webcam (ya ejecutado)
❌ **core/templates/base.html** - Template duplicado (public tiene su propio base)
❌ **public/templates/public/carrito.html** - Página obsoleta (reemplazada por sidebar)
❌ **public/tests.py** - Archivo vacío sin tests
❌ **core/tests.py** - Archivo vacío sin tests
❌ **public/models.py** - Archivo vacío (modelos están en core)

## Notas Técnicas

### Separación Core vs Public
- **Core**: Gestiona modelos y admin, NO tiene estáticos propios
- **Public**: Toda la UI pública, CSS, JS, templates del cliente
- NO mezclar templates entre apps (cada una tiene su estructura)

### Carrito de Compras
- **Estado cliente**: Solo localStorage (array de {id, nombre, precio, cantidad})
- **Sidebar**: Renderiza desde localStorage, no hay modelo "Carrito" en Django
- **Persistencia**: Solo al confirmar pedido (Pedido/PedidoItem se crean)
- **Stock**: Validado en servidor antes de crear pedido, descuento atómico

### Configuración de Templates
- `settings.py` define `DIRS` solo para `public/templates`
- Templates de core funcionan por `APP_DIRS=True`
- No hay conflicto porque ambas apps tienen subdirectorios (admin/, public/)

### Filtros en Home
- Query params: `categoria`, `q`, `precio_min`, `precio_max`, `page`
- Queryset incremental: `qs = qs.filter(...).filter(...)`
- Categorías: agregadas con `values('categoria').annotate(total=Count('id'))`
- Preservar params en paginación: `filtros_qs = preserved_params.urlencode()`

### Sidebar Cart (Implementación)
**HTML** (base.html):
- `.cart-sidebar` con header/body/footer
- `#cartSidebarContent` para items dinámicos
- `.cart-sidebar-overlay` para backdrop

**CSS** (style.css):
- Position fixed, width 400px (100% en mobile)
- Slide desde right: -400px → 0
- Transiciones 0.3s ease
- Scrollbar custom

**JavaScript** (carrito.js):
- `renderizarCartSidebar()`: Lee localStorage, genera HTML
- `abrirCartSidebar()`: Añade clase 'active', bloquea scroll body
- `cerrarCartSidebar()`: Remueve clase, restaura scroll
- `eliminarDelCarrito(id)`: Filtra item, actualiza storage

## Seguridad

- CSRF token en todos los POST (Django default)
- `@login_required` en vistas administrativas
- Validación de stock antes de confirmar pedido
- `transaction.atomic()` para operaciones críticas
- Sanitización de inputs en formularios

## Performance

- Paginación (12 items/página) reduce carga
- Imágenes: solo 1 query para productos visibles
- Categorías: 1 query con aggregation (no N+1)
- LocalStorage: operaciones síncronas rápidas
- Assets estáticos: cacheables, versionables

## Próximos Pasos Sugeridos

### Funcional
- [ ] Migrar carrito 100% al servidor (session-based)
- [ ] Integración con pasarela de pago (MercadoPago)
- [ ] Notificaciones por email de pedido
- [ ] Sistema de cupones/descuentos
- [ ] Wishlist/favoritos
- [ ] Reseñas y calificaciones de productos
- [ ] Panel de seguimiento de pedidos para clientes

### Técnico
- [ ] Tests de integración completos
- [ ] Deploy a producción (Heroku/Railway/VPS)
- [ ] PostgreSQL en producción
- [ ] CDN para assets estáticos
- [ ] Compresión de imágenes automática
- [ ] Búsqueda full-text (PostgreSQL/Elasticsearch)
- [ ] Cache con Redis
- [ ] Logs estructurados
- [ ] Monitoring (Sentry)

### UX
- [ ] Agregar imágenes a items del sidebar cart
- [ ] Filtro activo=True en home (actualmente lista todos)
- [ ] Mejora de accesibilidad (ARIA labels completos)
- [ ] PWA con service worker para offline
- [ ] Comparador de productos
- [ ] Historial de navegación
- [ ] Recomendaciones basadas en vistas

## Contacto y Soporte

Para consultas técnicas, revisar:
1. Este Readme técnico
2. `Readme usuario.txt` para funcionalidades
3. `Readme_copilot.txt` para guía de AI agents
4. Código fuente comentado en `core/` y `public/`
