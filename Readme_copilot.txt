## Porta Informática – Registro técnico vivo (IA⇄IA)

Este archivo resume el estado ACTUAL (post refactors recientes) para que otro agente pueda continuar sin releer toda la base.

### 1. Stack y apps
- Django 5.2.x – DB SQLite en desarrollo.
- Apps reales: `core` (modelos, carga/admin) y `public` (catálogo + UI). Archivo mencionaba `productos` pero NO existe como app separada.
- Nuevo dominio funcional: persistencia de pedidos (modelo agregado).

### 2. Modelos clave (core/models.py)
Producto(nombre, descripcion, precio, stock, imagen, activo, categoria)
Perfil(user OneToOne, telefono, direccion)
Pedido(user FK nullable, creado datetime, nombre_cliente, telefono, direccion, metodo_pago, total, mensaje_whatsapp)
PedidoItem(pedido FK, producto FK nullable, nombre congelado, cantidad, precio_unitario, subtotal)
Notas:
- `total` recalculado server-side en confirmación (no confiar en JSON).
- `mensaje_whatsapp` almacena snapshot del texto enviado (trazabilidad/auditoría).

### 3. Carrito / Pedido (estado híbrido)
- Origen cliente: localStorage key `pedido` (array de items {id, nombre, precio, cantidad}).
- Acciones JS centralizadas en `public/static/js/carrito.js`:
	- agregarAlPedido / actualizarContadorCarrito
	- formatearPedidoMensaje (render markdown-like → texto plano WhatsApp)
	- enviarPedidoWhatsApp (usa `wa.me` con encodeURIComponent)
	- enviarPedidoServidor (shadow write → POST /pedido/confirmar/ con JSON)
- Vista `confirmar_pedido` crea Pedido + PedidoItems y retorna `{pedido_id,total}`.

### 4. Catálogo y filtros (`public/views.py::home`)
- Parámetros soportados: categoria, q, precio_min, precio_max, page.
- Paginación: `Paginator(..., 12)` exponiendo `page_obj` + `filtros_qs` para enlaces.
- Categorías: consulta separada global (`values('categoria').annotate(total=Count('id'))`).
- TODO futuro: aplicar filtro `activo=True` (definido en modelo, no usado aún).

### 5. Front refactor reciente
- `base.html`: unificado header + nav + footer; agregado `<main>` y variables de color via CSS (:root en `style.css`).
- Eliminada doble carga de `carrito.js`.
- Footer estructurado (3 columnas responsive) + links tel.
- Agregada grilla responsiva productos (col-lg-3 col-md-4 col-sm-6 col-6) + `loading="lazy"`.
- Botones “Agregar al pedido” migrados a data-attributes + listener delegado (sin inline JS).
- Se añadieron templates antes vacíos: `servicios.html`, `contacto.html` (placeholders estructurados).

### 6. Endpoint nuevo
POST `/pedido/confirmar/` (login requerido) JSON schema:
{
	"items": [{"id":int, "cantidad":int, "precio":float, "nombre":str}],
	"cliente": {"nombre":str, "telefono":str, "direccion":str, "metodo_pago":str},
	"mensaje": str (opcional)
}
Server recalcula precio usando Producto si existe. Valores faltantes → saneados.

### 7. Admin (`core/admin.py`)
- Inline de PedidoItem en PedidoAdmin (readonly subtotal, etc.).
- Fields protegidos: total, creado, mensaje_whatsapp.

### 8. Seguridad / Consideraciones
- No hay control de stock al confirmar pedido (riesgo: sobreventa). Siguiente paso: validar y opcionalmente decrementar.
- Sin verificación de integridad de precios cliente → ya se sobreescribe con precio real si hay FK.
- CSRF en fetch: se toma cookie `csrftoken` (Django default). Si se añade API externa → revisar.

### 9. UI pendiente / mejoras candidatas
- Ajustar altura hero + recorte consistente (clases `hero-carousel`, `hero-img`).
- Jerarquía tipográfica unificada (clases utilitarias no creadas aún: `.titulo-seccion`).
- Añadir `loading="lazy"` también a imágenes del logo secundarias (si existieran).
- Accesibilidad: labels y `aria-live` para contador carrito.

### 10. Futuro: transición carrito → modelo completo
Estrategia recomendada:
1. Shadow write (implementado).
2. Lectura server-side opcional: endpoint GET /pedido/borrador/ devolviendo items.
3. Reemplazo progresivo de localStorage por API + fallback offline.

### 11. Puntos de extensión seguros
- Filtros extra: agregar param -> encadenar al queryset ANTES de paginar.
- Estados de Pedido: campo `estado` (choices) + índice.
- Historial de precio: nueva tabla si se requiere auditoría profunda.

### 12. Comandos habituales
env\\Scripts\\activate
python manage.py migrate
python manage.py runserver

### 13. Technical debt actual (orden)
1. Falta control de stock en confirmación.
2. Falta filtro `activo=True` en catálogo.
3. No hay tests de creación de Pedido.
4. Formularios públicos sin validación server-side (contacto placeholder).
5. No hay paginación en Admin para productos (si crece list_display).

### 14. Quick sanity diff vs viejo README
- Eliminado concepto de app `productos` (no existe).
- Botón carrito ya no usa inline JS.
- Pedido ahora persiste.

Fin del snapshot. Actualizar este archivo cada vez que cambie un flujo transversal (carrito, catálogo, modelos). 
