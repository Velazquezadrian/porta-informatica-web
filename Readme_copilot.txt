# Copilot Instructions – porta-informatica-web## Porta Informática – Registro técnico vivo (IA⇄IA)



**Guía concisa y actualizada (Nov 2025) para AI agents contribuyendo a este catálogo Django e-commerce.**Este archivo resume el estado ACTUAL (post refactors recientes) para que otro agente pueda continuar sin releer toda la base.



Focus en respetar separación admin vs público, flujo de datos actual, y convenciones de nomenclatura en español.### 1. Stack y apps

- Django 5.2.x – DB SQLite en desarrollo.

---- Apps reales: `core` (modelos, carga/admin) y `public` (catálogo + UI). Archivo mencionaba `productos` pero NO existe como app separada.

- Nuevo dominio funcional: persistencia de pedidos (modelo agregado).

## 1. Arquitectura General

### 2. Modelos clave (core/models.py)

### Apps y SeparaciónProducto(nombre, descripcion, precio, stock, imagen, activo, categoria)

- **core/**: Modelos de datos + admin + gestión internaPerfil(user OneToOne, telefono, direccion)

- **public/**: Catálogo + UI del cliente + carrito + checkoutPedido(user FK nullable, creado datetime, nombre_cliente, telefono, direccion, metodo_pago, total, mensaje_whatsapp)

- **NO mezclar** templates ni estáticos entre appsPedidoItem(pedido FK, producto FK nullable, nombre congelado, cantidad, precio_unitario, subtotal)

Notas:

### Configuración de Templates- `total` recalculado server-side en confirmación (no confiar en JSON).

- `portaside/settings.py` define `DIRS` solo para `public/templates`- `mensaje_whatsapp` almacena snapshot del texto enviado (trazabilidad/auditoría).

- Templates de `core` funcionan por `APP_DIRS=True` (viven en `core/templates/admin/`)

- Cada app tiene subdirectorios propios → no hay conflicto de nombres### 3. Carrito / Pedido (estado híbrido)

- Origen cliente: localStorage key `pedido` (array de items {id, nombre, precio, cantidad}).

### Flujo de Datos del Carrito- Acciones JS centralizadas en `public/static/js/carrito.js`:

1. **Cliente (localStorage)**: Items guardados en navegador como JSON array	- agregarAlPedido / actualizarContadorCarrito

2. **Sidebar Cart**: UI lateral renderizada dinámicamente desde localStorage	- formatearPedidoMensaje (render markdown-like → texto plano WhatsApp)

3. **Confirmación**: Al checkout, datos POST a servidor	- enviarPedidoWhatsApp (usa `wa.me` con encodeURIComponent)

4. **Servidor (Pedido/PedidoItem)**: Persistencia con validación de stock y descuento atómico	- enviarPedidoServidor (shadow write → POST /pedido/confirmar/ con JSON)

- Vista `confirmar_pedido` crea Pedido + PedidoItems y retorna `{pedido_id,total}`.

---

### 4. Catálogo y filtros (`public/views.py::home`)

## 2. Modelos de Datos (core/models.py)- Parámetros soportados: categoria, q, precio_min, precio_max, page.

- Paginación: `Paginator(..., 12)` exponiendo `page_obj` + `filtros_qs` para enlaces.

### Producto- Categorías: consulta separada global (`values('categoria').annotate(total=Count('id'))`).

Campos principales: `nombre`, `descripcion`, `precio`, `stock`, `imagen`, `activo`, `categoria`, `marca`, `modelo`- TODO futuro: aplicar filtro `activo=True` (definido en modelo, no usado aún).

Campos opcionales: `caracteristicas`, `especificaciones_tecnicas`, `conectividad`, `alimentacion`, `garantia`, `compatibilidad`

### 5. Front refactor reciente

**⚠️ Importante**: Usar `activo=True` como filtro en queries del catálogo público- `base.html`: unificado header + nav + footer; agregado `<main>` y variables de color via CSS (:root en `style.css`).

- Eliminada doble carga de `carrito.js`.

### Perfil- Footer estructurado (3 columnas responsive) + links tel.

Relación OneToOne con User: `telefono`, `direccion`- Agregada grilla responsiva productos (col-lg-3 col-md-4 col-sm-6 col-6) + `loading="lazy"`.

**Acceso defensivo**: `getattr(request.user, 'perfil', None)`- Botones “Agregar al pedido” migrados a data-attributes + listener delegado (sin inline JS).

- Se añadieron templates antes vacíos: `servicios.html`, `contacto.html` (placeholders estructurados).

### Pedido

Campos: `user` (FK nullable), `creado`, `nombre_cliente`, `telefono`, `direccion`, `metodo_pago`, `total`, `mensaje_whatsapp`### 6. Endpoint nuevo

**Nota**: `total` se recalcula server-side, no confiar en JSON del clientePOST `/pedido/confirmar/` (login requerido) JSON schema:

{

### PedidoItem	"items": [{"id":int, "cantidad":int, "precio":float, "nombre":str}],

Relación con Pedido y Producto (FK nullable)	"cliente": {"nombre":str, "telefono":str, "direccion":str, "metodo_pago":str},

Campos congelados: `nombre`, `precio_unitario`, `subtotal` (snapshot al momento de compra)	"mensaje": str (opcional)

}

---Server recalcula precio usando Producto si existe. Valores faltantes → saneados.



## 3. Sistema de Carrito (Arquitectura Híbrida)### 7. Admin (`core/admin.py`)

- Inline de PedidoItem en PedidoAdmin (readonly subtotal, etc.).

### Cliente (localStorage)- Fields protegidos: total, creado, mensaje_whatsapp.

**Key**: `'pedido'`

**Estructura**: `[{id, nombre, precio, cantidad}, ...]`### 8. Seguridad / Consideraciones

**Ubicación código**: `public/static/js/carrito.js`- No hay control de stock al confirmar pedido (riesgo: sobreventa). Siguiente paso: validar y opcionalmente decrementar.

- Sin verificación de integridad de precios cliente → ya se sobreescribe con precio real si hay FK.

**Funciones principales**:- CSRF en fetch: se toma cookie `csrftoken` (Django default). Si se añade API externa → revisar.

- `agregarAlPedido(nombre, precio, id)`: Añade o incrementa cantidad

- `actualizarContadorCarrito()`: Actualiza badge del navbar### 9. UI pendiente / mejoras candidatas

- `eliminarDelCarrito(id)`: Remueve item específico- Ajustar altura hero + recorte consistente (clases `hero-carousel`, `hero-img`).

- `vaciarPedido()`: Limpia todo el carrito- Jerarquía tipográfica unificada (clases utilitarias no creadas aún: `.titulo-seccion`).

- Añadir `loading="lazy"` también a imágenes del logo secundarias (si existieran).

### Sidebar Cart (UI)- Accesibilidad: labels y `aria-live` para contador carrito.

**HTML**: Definido en `public/templates/public/base.html`

- Contenedor: `.cart-sidebar` con `id="cartSidebar"`### 10. Futuro: transición carrito → modelo completo

- Content: `#cartSidebarContent` (renderizado dinámico)Estrategia recomendada:

- Overlay: `.cart-sidebar-overlay` con `id="cartOverlay"`1. Shadow write (implementado).

2. Lectura server-side opcional: endpoint GET /pedido/borrador/ devolviendo items.

**CSS**: `public/static/css/style.css` (~180 líneas de estilos)3. Reemplazo progresivo de localStorage por API + fallback offline.

- Position fixed, width 400px desktop / 100% mobile

- Animación slide: `right: -400px` → `right: 0` con clase `.active`### 11. Puntos de extensión seguros

- Transiciones 0.3s ease- Filtros extra: agregar param -> encadenar al queryset ANTES de paginar.

- Estados de Pedido: campo `estado` (choices) + índice.

**JavaScript**: Funciones en `carrito.js`- Historial de precio: nueva tabla si se requiere auditoría profunda.

- `renderizarCartSidebar()`: Lee localStorage, genera HTML

- `abrirCartSidebar()`: Añade clase active, bloquea scroll body### 12. Comandos habituales

- `cerrarCartSidebar()`: Remueve clase, restaura scrollenv\\Scripts\\activate

- Event listeners: openCartBtn, closeCartBtn, overlay, clearCartBtnpython manage.py migrate

python manage.py runserver

### Persistencia Servidor

**Endpoint**: `POST /pedido/confirmar/` (requiere login)### 13. Technical debt actual (orden)

**Vista**: `public/views.py::confirmar_pedido()`1. Falta control de stock en confirmación.

2. Falta filtro `activo=True` en catálogo.

**Flujo**:3. No hay tests de creación de Pedido.

1. Recibe JSON con items + datos cliente4. Formularios públicos sin validación server-side (contacto placeholder).

2. Valida stock disponible5. No hay paginación en Admin para productos (si crece list_display).

3. `transaction.atomic()` para crear Pedido + PedidoItems

4. Descuenta stock automáticamente### 14. Quick sanity diff vs viejo README

5. Retorna `{pedido_id, total}` o error 409 si falta stock- Eliminado concepto de app `productos` (no existe).

- Botón carrito ya no usa inline JS.

**⚠️ Seguridad**: Siempre usar precio de `Producto` real, no el del cliente- Pedido ahora persiste.



---Fin del snapshot. Actualizar este archivo cada vez que cambie un flujo transversal (carrito, catálogo, modelos). 


## 4. Vistas Públicas (public/views.py)

### home
**URL**: `/`
**Filtros soportados**: `categoria`, `q`, `precio_min`, `precio_max`, `page`
**Paginación**: 12 productos por página
**Categorías**: Query con aggregation `values('categoria').annotate(total=Count('id'))`
**Productos destacados**: 8 aleatorios en página 1 sin filtros

### producto_detalle
**URL**: `/producto/<int:producto_id>/`
**Patrón**: Usar `get_object_or_404(Producto, id=producto_id)`

### pedido
**URL**: `/pedido/`
**Función**: Página de checkout con formulario
**Auto-complete**: Teléfono y dirección si usuario tiene perfil

### confirmar_pedido
**URL**: `POST /pedido/confirmar/`
**Decoradores**: `@login_required`, `@require_POST`
**Ver**: Sección "Persistencia Servidor" arriba

### buscar
**URL**: `/buscar/?q=...&marca=...`
**Búsqueda**: En nombre, descripción, categoría, marca
**Sidebar**: Lista de marcas para filtrar

### categoria_detalle
**URL**: `/c/<categoria>/<subcategoria>/`
**Filtro**: `categoria__iexact=subcategoria.replace('-', ' ')`

---

## 5. Frontend (Templates y Assets)

### Base Template (public/templates/public/base.html)
**Estructura**:
- Header: Logo, navbar, buscador, cart icon
- Main: `{% block content %}`
- Cart Sidebar: HTML completo incluido
- WhatsApp flotante: Bottom-right
- Footer: 3 columnas

**Scripts cargados**:
- `menu_dinamico.js`: Menú de categorías dinámico
- `carrito.js`: Toda la lógica del carrito

### CSS (public/static/css/style.css)
**Variables**:
```css
:root {
  --color-primario: #FF6B35;
  --color-primario-hover: #E65A2F;
  --color-secundario: #2C3E50;
}
```

**Secciones importantes**:
- Gradientes de fondo en todas las páginas
- Cards con hover effects
- Sidebar cart (~180 líneas)
- WhatsApp button con animación pulse
- Responsive: `@media (max-width: 768px)`

### JavaScript

**menu_dinamico.js**:
- Genera menú de categorías desde DOM
- Reglas de normalización con regex
- Ejemplo: `addSubcategory('Joystick')` en Periféricos

**carrito.js** (funciones clave ya descritas en sección 3)

---

## 6. Patrones de Extensión

### Nuevo filtro en catálogo
1. Añadir query param en `home()`
2. Validar input
3. Encadenar filter al queryset: `qs = qs.filter(...)`
4. Preservar en paginación con `preserved_params`

### Nuevo campo en carrito localStorage
1. Modificar `agregarAlPedido()` para incluir campo
2. Actualizar `renderizarCartSidebar()` para mostrarlo
3. Modificar `confirmar_pedido()` para procesarlo
4. **Retrocompatibilidad**: Verificar existencia antes de usar

### Nueva categoría
1. Editar `core/models.py` → `CATEGORIA_CHOICES`
2. Migrar: `makemigrations` + `migrate`
3. Editar `menu_dinamico.js` para incluirla en menú

---

## 7. Archivos Eliminados (Nov 2025)

**NO referenciar estos archivos (ya no existen)**:
- ❌ `update_c270.py` (script one-off)
- ❌ `corregir_categorias.py` (script one-off)
- ❌ `core/templates/base.html` (duplicado)
- ❌ `public/templates/public/carrito.html` (obsoleto, reemplazado por sidebar)
- ❌ `public/tests.py` (vacío)
- ❌ `core/tests.py` (vacío)
- ❌ `public/models.py` (vacío)

---

## 8. Technical Debt Actual

### Prioridad Alta:
1. ⚠️ Falta filtro `activo=True` en catálogo home
2. ⚠️ Import faltante `get_object_or_404` en public/views.py
3. ⚠️ Vista servicios: typo en nombre de template

### Prioridad Media:
4. Sidebar sin imágenes de productos
5. No se puede editar cantidad en sidebar
6. Paginación sin order_by genera warning

---

## 9. Comandos Útiles

```bash
# Entorno
env\Scripts\activate
pip install -r requirements.txt

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Servidor
python manage.py runserver

# Tests
python manage.py test public.tests_pedido
```

---

## 10. Errores Comunes

### Sidebar no abre
- Verificar `#openCartBtn` existe
- Verificar event listener en carrito.js
- Revisar console por errores JS

### Perfil no existe
- Usar `getattr(request.user, 'perfil', None)`
- O crear con `get_or_create()`

### Stock negativo
- Ya resuelto con validación en `confirmar_pedido()`

---

## 11. Seguridad

- CSRF: Django default + `getCookie('csrftoken')` en fetch
- Login: `@login_required` en admin, opcional en público
- Stock: Validado server-side con `transaction.atomic()`
- Precios: Siempre usar valor de BD, nunca del cliente

---

## 12. Referencias

- **Código carrito**: `public/static/js/carrito.js`
- **Modelos**: `core/models.py`
- **Config templates**: `portaside/settings.py`
- **Rutas públicas**: `public/urls.py`
- **Tests**: `public/tests_pedido.py`
- **Docs completa**: `Readme tecnico.txt`
- **Manual usuario**: `Readme usuario.txt`

---

**Última actualización**: Noviembre 2025
**Django**: 5.2.6
**Estado**: Desarrollo local

Mantener estas convenciones. Consultar `Readme tecnico.txt` para detalles adicionales.
