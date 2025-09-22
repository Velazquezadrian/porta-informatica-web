# Porta Informática – Registro técnico completo

## Proyecto
- Django
- Apps: `public`, `core`, `productos`
- Entorno virtual: `.venv`
- Repositorio: https://github.com/Velazquezadrian/porta-informatica-web

## Configuración inicial
- `git init`, `.gitignore`, `requirements.txt`, `README.md`
- Configuración de identidad Git
- Push inicial a GitHub
- Activación de entorno virtual
- Generación de `requirements.txt` con `pip freeze`

## Diseño visual
- Hero con fondo + overlay
- Cards de servicios con AOS.js
- Tipografía moderna (Poppins/Inter)
- Botones con clases `.btn-primary`, `.btn-secondary`
- Footer con contacto y redes
- Estilos en `static/style.css`

## Flujo de “casi carrito”
- Botón “Agregar al pedido” → guarda en `localStorage`
- Vista `/pedido/` con resumen + formulario
- Botón final que abre WhatsApp con `window.open()`
- Script JS para agregar productos y generar mensaje

## Estructura de templates
- `base.html`
- `home.html`
- `servicios.html`
- `contacto.html`
- `pedido.html`
- Carpeta: `templates/public/`

## Catálogo dinámico
- Modelo `Producto` con: `nombre`, `description`, `precio`, `stock`, `imagen`, `es_nuevo`
- Vista `catalogo()` con `Producto.objects.all()`
- Loop `{% for producto in productos %}` en template
- Botón con `onclick="agregarAlPedido('{{ producto.nombre }}')"`

## Panel interno
- Vista protegida `subir_producto` con formulario
- Vista protegida `lista_productos` con listado
- URLs en `core/urls.py`: `admin/subir/`, `admin/lista/`
- Decoradores `@login_required`

## Documentación
- `README.md` público con instalación y tecnologías
- `README_DEV.md` técnico con estructura y flujo
- `README_COPILOT.md` como prompt interno

## Pendientes
- Agregar campo de cantidad por producto
- Validar formulario antes de enviar
- Botón “Vaciar pedido”
- Optimizar diseño responsive
- Subir capturas al README público
- Internacionalización opcional
- Integración con carrito real (futuro)
