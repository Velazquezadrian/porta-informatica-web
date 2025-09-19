
---

## 📗 2. README de usuario (manual básico para uso interno)

Este archivo explica cómo usar el sistema desde el navegador, sin entrar en código.

```markdown
# Panel de productos - Porta Informática

## 🔐 Acceso

1. Ingresar a: `http://127.0.0.1:8000/admin/`
2. Iniciar sesión con usuario y contraseña

## 📦 Cargar producto

1. Ir a: `http://127.0.0.1:8000/admin/subir/`
2. Completar nombre, descripción, precio, stock, imagen
3. Presionar "Guardar"

## 📋 Ver productos cargados

1. Ir a: `http://127.0.0.1:8000/admin/lista/`
2. Ver tabla con todos los productos
3. Se muestra nombre, precio, stock, imagen y estado

## 🧠 Recomendaciones

- Usar imágenes claras y livianas
- Mantener precios actualizados
- Desactivar productos sin stock

## 🛠️ Panel técnico

Si tenés acceso al panel de Django (`/admin/`), podés editar productos directamente desde ahí.
