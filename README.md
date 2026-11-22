# Trabajo Final Python — Sistema de Gestión de Inventario (Python + SQLite)

Aplicación de consola desarrollada en Python utilizando `sqlite3` para persistir productos en `inventario.db` y `colorama` para mejorar la lectura en terminal.

## Funcionalidades

- **Registrar producto:** Alta con validación de nombre obligatorio, cantidad entera no negativa y precio decimal no negativo (admite punto o coma).
- **Visualizar productos:** Listado en tabla con subtotal por producto (`cantidad * precio`) y valor total del inventario.
- **Actualizar producto:** Modificación por `ID` permitiendo conservar los valores actuales presionando `Enter`.
- **Eliminar producto:** Baja por `ID` con confirmación (`s/n`).
- **Buscar producto:** Consulta por `ID`, `Nombre` o `Categoría`.
- **Reporte de stock crítico:** Muestra productos con `cantidad <= límite` indicado por el usuario, resaltando los que están agotados (`0` unidades).

## Instalación y ejecución

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
