Readme Técnico - porta-informatica-web

## Descripción General

Este proyecto es una aplicación web desarrollada con Django, orientada a la gestión y visualización de productos informáticos. El sistema cuenta con una sección administrativa y una sección pública, permitiendo la administración de productos y la visualización de un catálogo para los usuarios.

## Estructura del Proyecto

- **core/**: App principal para la administración de productos.
   - `models.py`: Define los modelos de datos (productos, categorías, etc).
   - `admin.py`: Configuración del panel de administración de Django.
   - `forms.py`: Formularios para la gestión de productos.
   - `views.py`: Vistas para la lógica administrativa.
   - `urls.py`: Rutas de la app administrativa.
   - `templates/admin/`: Plantillas HTML para la administración.

- **public/**: App para la parte pública del sitio.
   - `models.py`: Modelos públicos (si aplica).
   - `views.py`: Vistas para mostrar el catálogo, contacto, servicios, etc.
   - `urls.py`: Rutas públicas.
   - `static/css/style.css`: Estilos para la parte pública.
   - `templates/public/`: Plantillas HTML públicas (home, catálogo, contacto, servicios, etc).

- **media/productos/**: Carpeta donde se almacenan las imágenes de los productos subidos.

- **portaside/**: Configuración principal del proyecto Django.
   - `settings.py`: Configuración general, bases de datos, apps instaladas, rutas de archivos estáticos y media.
   - `urls.py`: Rutas principales del proyecto.

- **requirements.txt**: Lista de dependencias del proyecto (Django, Pillow, etc).

- **db.sqlite3**: Base de datos SQLite utilizada en desarrollo.

- **env/**: Entorno virtual de Python para aislar dependencias.

## Funcionalidades Implementadas

- Gestión de productos desde el panel de administración (alta, baja, modificación, carga de imágenes).
- Visualización pública de productos en formato catálogo.
- Páginas públicas: home, contacto, servicios, pedido.
- Separación de lógica y plantillas entre administración y público.
- Manejo de archivos estáticos y media.

## Tecnologías Utilizadas

- Python 3.13
- Django 5.2.6
- Pillow (para manejo de imágenes)
- SQLite (base de datos en desarrollo)

## Estructura de Archivos Clave

- `manage.py`: Script de gestión de Django.
- `requirements.txt`: Dependencias del proyecto.
- `Readme tecnico.txt`: Este archivo.
- `Readme usuario.txt`: Manual de usuario final.
- `Readme_copilot.txt`: Prompt para Copilot.

## Notas

- El proyecto sigue la estructura estándar de Django, con apps separadas para administración y público.
- El entorno virtual debe activarse antes de ejecutar comandos de Django.
- Las imágenes de productos se almacenan en `media/productos/`.

## Próximos pasos sugeridos

- Implementar autenticación de usuarios para la administración.
- Mejorar validaciones y mensajes de error en formularios.
- Agregar tests automatizados.
- Desplegar en un entorno de producción.
