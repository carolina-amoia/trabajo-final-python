# Trabajo Final - Curso de Python

Repositorio correspondiente al proyecto final obligatorio para la aprobación del curso de programación en Python. Consiste en un sistema de gestión de inventario desarrollado bajo los requerimientos técnicos solicitados.

## 🚀 Características del Proyecto
- **Base de Datos SQLite (`inventario.db`):** Almacenamiento local estructurado con la tabla `productos` (ID autoincremental, nombre, descripción, cantidad, precio y categoría).
- **Gestión CRUD Completa:** 
  - Registro de nuevos productos con validación de datos.
  - Visualización en formato de tabla organizada en consola.
  - Actualización de registros mediante su ID único.
  - Eliminación segura de productos mediante ID con confirmación.
- **Búsqueda Avanzada:** Filtrado por ID, nombre o categoría.
- **Reportes de Stock Crítico:** Generación de listados filtrados por un límite máximo especificado por el usuario.
- **Modularización y Buenas Prácticas:** Código estructurado en funciones independientes, con comentarios educativos explicativos y manejo de errores.

## 🛠️ Requisitos Técnicos
- Python 3.x
- Librería estándar `sqlite3` (no requiere instalaciones externas adicionales).

## ⚙️ ¿Cómo ejecutar la aplicación?
1. Clona este repositorio o descarga los archivos en tu computadora.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta el siguiente comando:
   ```bash
   python app_inventario.py
