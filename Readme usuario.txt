# 🛒 Manual de Usuario - Porta Informática

## Tienda Online de Productos Informáticos---



---## 📗 2. README de usuario (manual básico para uso interno)



## 📱 Para Clientes (Uso de la Tienda)Este archivo explica cómo usar el sistema desde el navegador, sin entrar en código.



### 🏠 Navegación General```markdown

# Panel de productos - Porta Informática

**Acceder a la tienda**: `http://127.0.0.1:8000/`

## 🔐 Acceso

La página principal muestra:

- 🎯 Carrusel de productos destacados aleatorios1. Ingresar a: `http://127.0.0.1:8000/admin/`

- 📦 Catálogo completo de productos2. Iniciar sesión con usuario y contraseña

- 🔍 Barra de búsqueda en el header

- 📑 Menú de categorías desplegable## 📦 Cargar producto

- 🛒 Icono del carrito con contador de items

1. Ir a: `http://127.0.0.1:8000/admin/subir/`

### 🔍 Buscar Productos2. Completar nombre, descripción, precio, stock, imagen

3. Presionar "Guardar"

**Opción 1: Búsqueda rápida**

1. Escribir en la barra de búsqueda del header## 📋 Ver productos cargados

2. Presionar Enter o hacer clic en el ícono de lupa

3. Ver resultados filtrados1. Ir a: `http://127.0.0.1:8000/admin/lista/`

2. Ver tabla con todos los productos

**Opción 2: Navegar por categorías**3. Se muestra nombre, precio, stock, imagen y estado

1. Hacer clic en el menú "Categorías" del header

2. Seleccionar categoría principal (ej: Gaming, Periféricos, Notebook)## 🧠 Recomendaciones

3. Elegir subcategoría (ej: Mouse Gamer, Teclado, Logitech)

4. Ver productos de esa categoría específica- Usar imágenes claras y livianas

- Mantener precios actualizados

**Opción 3: Filtros avanzados**- Desactivar productos sin stock

En la página de búsqueda puedes filtrar por:

- 🏷️ Marca (sidebar izquierdo)## 🛠️ Panel técnico

- 💰 Rango de precio (mínimo y máximo)

- 📝 Palabras clave en nombre/descripciónSi tenés acceso al panel de Django (`/admin/`), podés editar productos directamente desde ahí.


### 🛍️ Agregar al Carrito

**Desde el catálogo**:
1. Hacer clic en el botón "Ver detalles" de cualquier producto
2. En la página del producto, elegir cantidad
3. Hacer clic en "Agregar al pedido"
4. Ver confirmación y actualización del contador del carrito

**Desde el detalle del producto**:
- Ver descripción completa
- Características técnicas
- Especificaciones
- Precio actual
- Stock disponible
- Imagen ampliada

### 🛒 Usar el Carrito Lateral (Sidebar)

**Abrir el carrito**:
- Hacer clic en el ícono 🛒 en la esquina superior derecha
- Se abrirá un panel lateral desde la derecha

**¿Qué muestra el sidebar?**
- Lista de todos los productos agregados
- Cantidad de cada producto
- Precio subtotal por item
- **Total general** en la parte inferior
- Botones de acción

**Gestionar items del carrito**:
- 🗑️ **Eliminar producto**: Hacer clic en el ícono de tacho de basura rojo junto a cada item
- 🧹 **Vaciar carrito completo**: Hacer clic en "Vaciar carrito" (pedirá confirmación)
- ❌ **Cerrar sidebar**: Hacer clic en la X, fuera del panel, o continuar comprando

**Realizar la compra**:
1. Revisar los productos en el sidebar
2. Hacer clic en "Realizar pedido" (botón naranja)
3. Se abrirá la página de checkout

### 📋 Completar el Pedido

**En la página de pedido** (`/pedido/`):

1. **Revisar resumen**: Ver lista completa de productos y total

2. **Completar datos del cliente**:
   - 👤 Nombre completo
   - 📱 Teléfono (WhatsApp) - formato: +54 + código de área + número
   - 📍 Dirección de entrega
   - 💳 Forma de pago (Efectivo, Transferencia, Tarjeta de crédito/débito)

3. **Enviar el pedido**:
   - **Opción A**: "Enviar pedido por WhatsApp" 
     - Se abrirá WhatsApp Web con el mensaje del pedido formateado
     - Incluye: productos, cantidades, precios, total, tus datos
     - Solo debes enviar el mensaje al número de la empresa
   
   - **Opción B**: "Guardar en servidor" (si estás registrado)
     - Guarda el pedido en el sistema
     - Valida stock disponible
     - Descuenta automáticamente del inventario
     - Genera número de pedido

4. **Después de enviar**:
   - El carrito se puede vaciar manualmente
   - Recibirás confirmación por WhatsApp
   - Coordinar entrega/retiro con la empresa

### 👤 Registro y Perfil (Opcional)

**Crear cuenta**:
1. Ir a `/registro/`
2. Completar usuario y contraseña
3. Hacer clic en "Registrarse"

**Ventajas de registrarse**:
- ✅ Auto-completado de datos en pedidos
- ✅ Historial de pedidos
- ✅ Seguimiento de compras
- ✅ Perfil editable

**Editar perfil**:
1. Iniciar sesión
2. Ir a "Perfil" en el menú
3. Hacer clic en "Editar perfil"
4. Actualizar teléfono y dirección
5. Guardar cambios

### 💬 Contacto y Soporte

**Botón flotante de WhatsApp**:
- Ubicado en la esquina inferior derecha (verde con pulso)
- Hacer clic para abrir chat directo con la empresa
- Disponible en todas las páginas

**Página de contacto**: `/contacto/`
- Dirección física de la tienda
- Teléfono de contacto
- Email
- Horarios de atención

**Página de servicios**: `/servicios/`
- Reparaciones
- Mantenimiento
- Asesoramiento técnico

---

## 🔧 Para Administradores (Gestión de la Tienda)

### 🔐 Acceso al Panel de Administración

**URL**: `http://127.0.0.1:8000/admin/`

**Credenciales**: Usuario y contraseña de superusuario

### 📦 Gestionar Productos

#### Ver todos los productos
1. Ir a: `http://127.0.0.1:8000/admin/core/producto/`
2. Ver tabla completa con:
   - Nombre
   - Precio
   - Stock
   - Categoría
   - Estado (activo/inactivo)
   - Imagen miniatura
3. Filtrar por categoría o buscar por nombre
4. Ordenar por columnas

#### Agregar nuevo producto
1. En la lista de productos, hacer clic en "Agregar producto +"
2. **Campos obligatorios**:
   - Nombre del producto
   - Descripción breve
   - Precio (formato: 1234.56)
   - Stock (cantidad disponible)
   - Categoría (seleccionar del menú)
   - Imagen (subir foto del producto)
   - Activo (tildar si quieres que aparezca en la tienda)

3. **Campos opcionales** (mejoran la experiencia del cliente):
   - Marca (ej: Logitech, HP, Asus)
   - Modelo (ej: MK270, F310)
   - Características (lista con viñetas)
   - Especificaciones técnicas (detalles completos)
   - Conectividad (ej: USB 2.0, Bluetooth 5.0)
   - Alimentación (ej: Batería recargable, USB)
   - Garantía (ej: 1 año oficial)
   - Compatibilidad (sistemas operativos, otros requisitos)

4. Hacer clic en "Guardar"

#### Editar producto existente
1. En la lista, hacer clic en el nombre del producto
2. Modificar los campos necesarios
3. **Opciones al guardar**:
   - "Guardar": Guarda y vuelve a la lista
   - "Guardar y continuar editando": Guarda pero sigue en el formulario
   - "Guardar y agregar otro": Guarda y abre formulario nuevo

#### Desactivar producto (sin eliminarlo)
1. Editar el producto
2. Destildar la casilla "Activo"
3. Guardar
4. El producto ya no aparecerá en la tienda pero se mantiene en la base de datos

#### Eliminar producto permanentemente
1. Seleccionar producto(s) en la lista (checkbox)
2. En "Acción", elegir "Eliminar productos seleccionados"
3. Confirmar eliminación
4. ⚠️ **Precaución**: Esto borra el producto y su imagen del servidor

### 📊 Gestionar Pedidos

#### Ver pedidos recibidos
1. Ir a: `http://127.0.0.1:8000/admin/core/pedido/`
2. Ver lista con:
   - Número de pedido (#ID)
   - Fecha y hora
   - Cliente (usuario registrado o nombre ingresado)
   - Total del pedido
   - Estado

#### Ver detalle de un pedido
1. Hacer clic en el número de pedido
2. Ver información completa:
   - **Cliente**: Nombre, teléfono, dirección
   - **Items**: Productos, cantidades, precios unitarios, subtotales
   - **Total general**
   - **Método de pago**
   - **Mensaje de WhatsApp** enviado
   - **Usuario** (si estaba registrado)

#### Filtrar pedidos
- Por fecha de creación
- Por usuario
- Por rango de total
- Ordenar por cualquier columna

### 👥 Gestionar Usuarios y Perfiles

#### Ver usuarios registrados
1. Ir a: `http://127.0.0.1:8000/admin/auth/user/`
2. Ver lista de usuarios con:
   - Nombre de usuario
   - Email
   - Fecha de registro
   - Estado (activo/staff/superuser)

#### Ver perfiles (datos adicionales)
1. Ir a: `http://127.0.0.1:8000/admin/core/perfil/`
2. Ver teléfono y dirección de cada usuario
3. Editar si es necesario

### 📈 Reportes y Estadísticas

En el panel principal (`/admin/`) puedes ver:
- Total de productos activos
- Total de pedidos recibidos
- Usuarios registrados

**Próximamente**: Dashboard con gráficos de ventas

### 🔧 Mantenimiento del Sistema

#### Actualizar stock masivamente
Opción 1: Desde el admin
1. Editar cada producto individualmente
2. Cambiar el campo "Stock"
3. Guardar

Opción 2: Script de carga masiva (avanzado)
1. Editar `importar_productos.py`
2. Actualizar datos de productos
3. Ejecutar: `python importar_productos.py`

#### Categorías disponibles
Las categorías están definidas en `core/models.py` (CATEGORIA_CHOICES):
- Computadoras: PC Armada
- Notebook: Lenovo, Asus, HP, Dell
- Impresoras: Laser, Multifunción, Matricial
- Almacenamiento: SSD, Disco Duro, Pendrive, Tarjeta SD, Discos Externos
- Conectividad: Router, Switch, Extensor Wifi, Adaptador Wifi
- Accesorios de PC: Fuente de Poder, Gabinete, Cooler/Ventilador
- Periféricos: Teclado, Mouse, Webcam, Parlante, Micrófono, Joystick
- Gaming: Mouse Gamer, Teclado Gamer, Auriculares Gamer, Silla Gamer
- Monitores: LCD, LED, Curvo, Gaming

**Agregar nueva categoría** (requiere programación):
1. Editar `core/models.py` → CATEGORIA_CHOICES
2. Editar `public/static/js/menu_dinamico.js`
3. Ejecutar: `python manage.py makemigrations` y `python manage.py migrate`

#### Respaldo de datos
```bash
# Backup de base de datos
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json
```

#### Limpiar imágenes no usadas
Las imágenes de productos eliminados quedan en `media/productos/`
Limpiarlas manualmente revisando qué archivos no están referenciados

---

## 🆘 Preguntas Frecuentes (FAQ)

### Para Clientes

**¿El carrito se guarda si cierro el navegador?**
Sí, el carrito usa localStorage del navegador. Se mantiene aunque cierres la pestaña o el navegador (mientras no borres los datos del navegador).

**¿Puedo comprar sin registrarme?**
Sí, puedes agregar productos al carrito y enviar el pedido por WhatsApp sin crear cuenta. El registro es opcional para mayor comodidad.

**¿Cómo sé si hay stock disponible?**
En la página de cada producto se muestra el stock actual. Al confirmar el pedido, el sistema valida automáticamente si hay suficiente stock.

**¿Puedo modificar cantidades en el carrito?**
Actualmente debes eliminar el producto del carrito y agregarlo nuevamente con la cantidad correcta desde la página del producto.

**¿Se descuenta el stock automáticamente?**
Sí, al completar el pedido con "Guardar en servidor", el stock se descuenta automáticamente de forma segura.

**¿Qué pasa si envío por WhatsApp solamente?**
El mensaje con tu pedido se envía a la empresa, pero el stock no se descuenta automáticamente hasta que la empresa confirme manualmente en el sistema.

### Para Administradores

**¿Cómo accedo al panel admin?**
Debes tener credenciales de superusuario. Ir a `/admin/` e iniciar sesión.

**¿Puedo recuperar un producto eliminado?**
No, la eliminación es permanente. Mejor usar "desactivar" (destildar "Activo") para ocultar temporalmente.

**¿Las imágenes tienen límite de tamaño?**
No hay límite estricto, pero se recomienda imágenes de máximo 2MB y resolución 800x800px para velocidad.

**¿Cómo sé qué pedidos están pagos?**
Actualmente debes coordinar manualmente. El sistema guarda el método de pago seleccionado pero no verifica el pago.

**¿Puedo exportar la lista de productos?**
Desde el admin de Django puedes usar comandos avanzados. Para CSV básico, seleccionar productos y elegir acción de exportación (si está habilitada).

---

## 📞 Soporte Técnico

**Para clientes**:
- WhatsApp: Botón flotante verde en la tienda
- Email: (configurar email de contacto)
- Teléfono: (configurar teléfono)

**Para administradores**:
- Consultar `Readme tecnico.txt` para documentación técnica completa
- Consultar `Readme_copilot.txt` para trabajar con AI en el código
- Revisar código fuente en `core/` y `public/`

---

## 🎯 Tips y Mejores Prácticas

### Para dar mejor experiencia al cliente:
✅ Mantener stock actualizado en tiempo real
✅ Usar imágenes claras y de buena calidad
✅ Escribir descripciones completas con specs técnicas
✅ Responder rápido a pedidos por WhatsApp
✅ Actualizar precios regularmente
✅ Marcar productos sin stock como "inactivos" en vez de eliminarlos

### Para administrar mejor:
✅ Hacer backup semanal de la base de datos
✅ Revisar pedidos diariamente en `/admin/core/pedido/`
✅ Mantener categorías organizadas
✅ No mezclar productos de categorías diferentes
✅ Usar nombres descriptivos (incluir marca y modelo)
✅ Mantener consistencia en formato de precios

---

**Última actualización**: Noviembre 2025
**Versión del sistema**: Django 5.2.6
**Estado**: Producción (desarrollo local)
