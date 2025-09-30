# Copilot Instructions – porta-informatica-web

Concise, code-aware guide for AI agents contributing to this Django catalog app. Focus on respecting the admin vs público separation, existing data flow, and Spanish naming conventions.

## 1. Arquitectura (visión rápida)
- Apps: `core/` (gestión interna) y `public/` (catálogo y UI). No mezclar templates ni estáticos entre ellas.
- Config principal: `portaside/settings.py` define `DIRS` solo para `public/templates`; templates de `core` funcionan por `APP_DIRS=True`.
- Datos: `Producto` y `Perfil` están en `core/models.py`. El público importa desde `core` (no duplicar modelos en `public`).
- Estado cliente del “carrito”: solo en `localStorage` vía `public/static/js/carrito.js` (no hay modelo Pedido todavía).

## 2. Modelos relevantes
`Producto(nombre, descripcion, precio, stock, imagen, activo, categoria)` – usar `activo=True` como filtro cuando se agregue lógica de visibilidad.
`Perfil(user OneToOne, telefono, direccion)` – accesible como `request.user.perfil` (usar `getattr` defensivo, ya se hace en `pedido`).

## 3. Flujo de catálogo y filtros
Vista `public.views.home`:
- Acepta query params: `categoria`, `q`, `precio_min`, `precio_max`.
- Construye queryset incrementalmente. Mantener orden de filtros (idempotente) si se amplían.
- Categorías agregadas con `values('categoria').annotate(total=Count('id'))` – conservar este patrón para evitar múltiples queries.

## 4. Pedido (pseudo-carrito)
- JS expone `agregarAlPedido(nombre, precio, id)` que incrementa cantidades por `id`.
- Contador actualizado con `actualizarContadorCarrito()` en `DOMContentLoaded`.
- No hay validación de stock en cliente todavía; si se implementa, leer `Producto.stock` antes de permitir sumar.
- Envío final (WhatsApp) no está en repo; si se implementa, generar string desde localStorage (ver patrón existente de acumulación de items).

## 5. Autenticación y vistas protegidas
- Decorador `@login_required` en `core.views.subir_producto` y `lista_productos`.
- `pedido` también requiere login (`login_url='/login/'`). Mantener consistencia al agregar nuevas vistas internas.

## 6. Plantillas
- Admin: `core/templates/admin/*.html` (ej: `subir_producto.html`, `lista_productos.html`).
- Público: `public/templates/public/*.html` (ej: `home.html`, `pedido.html`, `producto_detalle.html`).
- Reutilizar bloques extendiendo un `base.html` (ver duplicidad potencial: hay un `base.html` en `core/templates` y otro en `public/templates/public/` — mantener cada uno en su ámbito, o decidir consolidación explícita antes de refactorizar).

## 7. Estáticos y media
- CSS y JS sólo en `public/static/`. No colocar assets nuevos en `core/static` salvo necesidad interna.
- Imágenes subidas van a `media/productos/` (derivado de `upload_to='productos/'`). Mantener rutas relativas en templates usando `{{ producto.imagen.url }}`.

## 8. Formularios
- Formulario de carga usa `ProductoForm` (en `core/forms.py`, no leído aquí pero asumir clásico ModelForm). Al crear nuevos forms seguir patrón español (ej: `FormularioPerfil`).

## 9. Patrones de extensión
- Nuevos filtros de catálogo: añadir query param -> validar -> encadenar `qs = qs.filter(...)` antes de construir categorías.
- Campo adicional del carrito: actualizar estructura en localStorage (respetar JSON array), mantener retrocompatibilidad (chequear propiedad antes de usarla).
- Paginación futura: usar `from django.core.paginator import Paginator` en `home` sin romper filtros existentes.

## 10. Errores y defensivos
- Usar `get_object_or_404` para detalle (ya se hace, aunque requiere importar en `public/views.py`).
- Acceso a perfil: usar `getattr(request.user, 'perfil', None)` como ya está.
- Validar `precio_min/max` convertibles a decimal antes de filtrar si se endurecen reglas.

## 11. Comandos esenciales (dev)
```
env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 12. Cambios sensibles (hacer con cuidado)
- Modificar `Producto`: implica migración y revisar templates (`home`, `producto_detalle`).
- Cambiar `MEDIA_ROOT/STATIC_URL`: actualizar referencias en templates y, si se despliega, configuración del servidor.
- Introducir modelo `Pedido`: decidir si se migra lógica desde localStorage gradualmente (fase de shadow write recomendable).

## 13. Próximas mejoras sugeridas (reales, no aspiracionales genéricos)
- Añadir filtro `activo=True` en `home` (actualmente lista todos).
- Import faltante: agregar `from django.shortcuts import get_object_or_404` en `public/views.py`.
- Corregir probable typo vista `servicios`: template referenced `public/servicio.html` pero archivo es `servicios.html`.

## 14. Referencias cruzadas
- Código cliente carrito: `public/static/js/carrito.js`.
- Seguridad básica: depender de `login_required`; no hay CSRF customizaciones.
- Single source of truth de productos: sólo `core.models.Producto`.

Mantener estas convenciones para evitar divergencias. Si algo no está documentado aquí, revisar `Readme tecnico.txt` y `Readme_copilot.txt` antes de introducir un nuevo patrón.
