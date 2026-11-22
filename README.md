# Sistema de Gestión de Inventario (Python + SQLite)

Aplicación de consola en Python que guarda los productos en `inventario.db` usando `sqlite3` y utiliza `colorama` para resaltar mensajes y alertas en terminal.

## Funcionalidades

- Registrar productos con validación de nombre obligatorio y números no negativos (admite punto o coma en precios).
- Visualizar todos los productos con subtotal por ítem y valor total del inventario.
- Actualizar productos por `ID` (presionar `Enter` mantiene el valor actual).
- Eliminar productos por `ID` con confirmación (`s/n`).
- Buscar productos por `ID`, `Nombre` o `Categoría`.
- Generar reporte de stock crítico (`cantidad <= límite`) resaltando productos agotados (`0` unidades).

## Uso

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
