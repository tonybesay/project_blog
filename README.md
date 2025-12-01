# 📰 Plataforma de Publicación de Artículos – Django

[![Website](https://img.shields.io/badge/🌐_Sitio_en_Producción-005BBB?style=for-the-badge)](https://appblog.tonybesaymh.com/)

Aplicación web desarrollada con **Django**, diseñada como un sistema completo de publicación y gestión de artículos.  
Incluye autenticación de usuarios, roles con permisos diferenciados, panel de administración, gestión de portadas, control editorial, secciones, comentarios y un flujo de publicación estructurado.

---

## 🚀 Características Principales

### 🧩 **Gestión de Artículos**
- Creación, edición y eliminación de artículos.
- Subida de imágenes de portada (media).
- Editor completo con campos de título, contenido, categoría, estado, etc.
- Artículos ordenados, paginados y mostrados en la página principal.

### 🛡️ **Sistema de Roles y Permisos**
- **Autor** → Puede crear y editar sus propios artículos.
- **Editor** → Revisa, aprueba o rechaza artículos.
- **Administrador** → Control total (Django Admin + permisos avanzados).
- **Usuario lector** → Puede ver artículos publicados y dejar comentarios.

### 👤 **Autenticación y Gestión de Usuarios**
- Registro y login personalizados.
- Perfíl de usuario editable.
- Señales para creación automática de perfiles.
- Sistema de likes y comentarios por usuario.

### 🖼️ **Frontend Limpio y Profesional**
- Plantillas hechas con **Bootstrap 5**.
- Hero de portada con presentación moderna.
- Listado de artículos con tarjetas visuales.
- Páginas detalladas responsivas y optimizadas.

### 💾 **Panel de Administración Mejorado**
- Django Admin personalizado.
- Filtros por estado, autor, fecha.
- Gestión de categorías y comentarios.

---

## 🏗️ Arquitectura del Proyecto

```plaintext
project_blog/
├── app_core/           # Home, vistas base, utilidades
├── app_article/        # Artículos, categorías, lógica editorial
├── app_review/         # Sistema de revisión y estados
├── app_user/           # Usuarios, perfiles, roles, señales
├── media/              # Portadas e imágenes subidas por usuarios
├── static/             # CSS, JS e imágenes estáticas
├── staticfiles/        # Archivos generados en collectstatic
├── templates/          # HTML con Bootstrap
├── project_blog/       # Configuración principal (settings, urls, wsgi)
└── requirements.txt    # Dependencias del proyecto
```

## 🛠️ Tecnologías Utilizadas

| Tecnología                     | Uso                                |
|--------------------------------|------------------------------------|
| **Python 3.12**                | Lenguaje base                      |
| **Django 5.x**                 | Framework principal                |
| **SQLite / PostgreSQL**        | Base de datos                      |
| **Bootstrap 5**                | Interfaz y estilos                 |
| **Nginx**                      | Servir archivos estáticos y media  |
| **Gunicorn**                   | WSGI en producción                 |
| **CloudPanel + DigitalOcean**  | Servidor y entorno de despliegue   |
| **Git + GitHub**               | Control de versiones               |
|--------------------------------|------------------------------------|
