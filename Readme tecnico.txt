# Porta Informática - Backend Django

## 🧱 Estructura del proyecto

- Proyecto principal: `portaside`
- App interna: `core`
- Entorno virtual: `env`
- Base de datos: SQLite (por defecto)

## 📦 Modelos

- `Producto`: nombre, descripción, precio, stock, imagen, activo

## 📄 Formularios

- `ProductoForm`: formulario basado en modelo para carga manual

## 🔐 Vistas protegidas

- `subir_producto`: carga de productos (requiere login)
- `lista_productos`: listado de productos cargados

## 🧩 URLs

- `/admin/subir/`: formulario de carga
- `/admin/lista/`: tabla de productos

## 🛠️ Requisitos

- Python 3.13
- Django
- Pillow (para imágenes)

## 🚀 Primer uso

```bash
python -m venv env
.\env\Scripts\activate
pip install django pillow
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
