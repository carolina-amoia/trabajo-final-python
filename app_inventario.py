import sqlite3  # Modulo estandar de Python para trabajar con bases de datos SQLite
from colorama import Fore, Style, init  # Colores y estilos para mejorar la lectura en consola

# Inicializo colorama con autoreset=True para que cada print vuelva al color normal automaticamente
init(autoreset=True)

# Nombre del archivo de base de datos local donde se guardan los productos
NOMBRE_DB = "inventario.db"


def inicializar_base_datos():
    """Crea la base 'inventario.db' y la tabla 'productos' si aun no existen."""
    try:
        # Uso 'with' para que la conexion se cierre bien y maneje la transaccion
        with sqlite3.connect(NOMBRE_DB) as conn:
            cursor = conn.cursor()
            # Creo la tabla con los campos y tipos pedidos en la consigna
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT
                )
            """)
            conn.commit()  # Guardo los cambios en la base de datos
    except sqlite3.Error as error:
        # Si hay algun problema con SQLite, muestro el error en rojo
        print(Fore.RED + f"✘ Error al inicializar la base de datos: {error}")


def pedir_texto(mensaje, obligatorio=False, valor_actual=None):
    """Pide un texto por consola; si hay valor_actual, dejar vacio conserva el actual."""
    while True:
        # Si estoy actualizando un producto, muestro el valor actual entre corchetes
        if valor_actual is not None:
            texto = input(f"{mensaje} [{valor_actual}]: ").strip()
            if texto == "":
                return valor_actual  # Si aprieta Enter sin escribir, dejo el dato que ya estaba
            return texto

        # Si es un registro nuevo, pido el dato y limpio espacios extras
        texto = input(f"{mensaje}: ").strip()
        if texto == "" and obligatorio:
            print(Fore.RED + "✘ Este campo es obligatorio y no puede quedar vacío.")
            continue  # Vuelvo a pedir el mismo campo
        return texto


def pedir_entero(mensaje, valor_actual=None):
    """Pide un numero entero mayor o igual a 0; si hay valor_actual, vacio lo conserva."""
    while True:
        if valor_actual is not None:
            texto = input(f"{mensaje} [{valor_actual}]: ").strip()
            if texto == "":
                return valor_actual
        else:
            texto = input(f"{mensaje}: ").strip()

        try:
            numero = int(texto)  # Convierto el texto ingresado a entero
            if numero < 0:
                print(Fore.RED + "✘ El número no puede ser negativo.")
                continue
            return numero
        except ValueError:
            # Captura el error si escriben letras o un formato que no es entero
            print(Fore.RED + "✘ Ingresá un número entero válido (ej: 10).")


def pedir_decimal(mensaje, valor_actual=None):
    """Pide un numero decimal >= 0 (acepta coma o punto); vacio conserva el actual."""
    while True:
        if valor_actual is not None:
            texto = input(f"{mensaje} [{valor_actual}]: ").strip()
            if texto == "":
                return valor_actual
        else:
            texto = input(f"{mensaje}: ").strip()

        try:
            # Reemplazo coma por punto para que funcione si alguien escribe por ejemplo 1500,50
            numero = float(texto.replace(",", "."))
            if numero < 0:
                print(Fore.RED + "✘ El precio no puede ser negativo.")
                continue
            return numero
        except ValueError:
            print(Fore.RED + "✘ Ingresá un número válido (ej: 1500.50 o 1500,50).")


def registrar_producto():
    """Solicita los datos del producto y lo inserta en la tabla 'productos'."""
    print(Fore.CYAN + Style.BRIGHT + "\n=== REGISTRAR NUEVO PRODUCTO ===")

    # Pido y valido cada campo antes de tocar la base de datos
    nombre = pedir_texto("Nombre del producto", obligatorio=True)
    descripcion = pedir_texto("Descripción (opcional)", obligatorio=False)
    cantidad = pedir_entero("Cantidad disponible")
    precio = pedir_decimal("Precio unitario")
    categoria = pedir_texto("Categoría (opcional)", obligatorio=False)

    try:
        with sqlite3.connect(NOMBRE_DB) as conn:
            cursor = conn.cursor()
            # Uso '?' como parametros para evitar inyeccion SQL
            cursor.execute(
                """
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
                """,
                (nombre, descripcion, cantidad, precio, categoria),
            )
            conn.commit()
        print(Fore.GREEN + f"✔ Producto '{nombre}' registrado con éxito.")
    except sqlite3.Error as error:
        print(Fore.RED + f"✘ Error al registrar el producto: {error}")


def visualizar_productos():
    """Consulta todos los productos, los muestra en tabla y calcula el valor total."""
    print(Fore.CYAN + Style.BRIGHT + "\n=== LISTADO DE PRODUCTOS ===")

    try:
        with sqlite3.connect(NOMBRE_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY id ASC")
            productos = cursor.fetchall()  # Traigo todas las filas encontradas
    except sqlite3.Error as error:
        print(Fore.RED + f"✘ Error al consultar los productos: {error}")
        return

    if not productos:
        print(Fore.YELLOW + "! No hay productos registrados en el inventario.")
        return

    # Encabezado de la tabla en consola
    print(Fore.CYAN + "=" * 92)
    print(
        Fore.CYAN
        + Style.BRIGHT
        + f"{'ID':<4} | {'NOMBRE':<18} | {'DESCRIPCIÓN':<18} | {'CANT':<5} | "
        f"{'PRECIO':<10} | {'CATEGORÍA':<13} | {'SUBTOTAL'}"
    )
    print(Fore.CYAN + "=" * 92)

    valor_total_inventario = 0.0  # Acumulador del valor total del stock

    for prod_id, nombre, desc, cant, precio, cat in productos:
        subtotal = cant * precio  # Valor de este producto segun su stock y precio unitario
        valor_total_inventario += subtotal

        # Recorto textos largos para que no rompan el alineado de las columnas
        desc_corta = (desc[:15] + "..") if desc and len(desc) > 17 else (desc or "-")
        cat_texto = (cat[:11] + "..") if cat and len(cat) > 13 else (cat or "Sin cat.")
        nombre_corto = (nombre[:16] + "..") if len(nombre) > 18 else nombre

        print(
            f"{prod_id:<4} | {nombre_corto:<18} | {desc_corta:<18} | {cant:<5} | "
            f"${precio:<9.2f} | {cat_texto:<13} | ${subtotal:.2f}"
        )

    print(Fore.CYAN + "=" * 92)
    print(
        Fore.GREEN
        + f"Total de productos: {len(productos)} | Valor total del inventario: ${valor_total_inventario:.2f}"
    )


def actualizar_producto():
    """Busca un producto por ID y permite actualizar sus campos manteniendo actuales si se deja vacio."""
    print(Fore.CYAN + Style.BRIGHT + "\n=== ACTUALIZAR PRODUCTO ===")
    visualizar_productos()  # Muestro primero el listado para que sea facil ubicar el ID

    prod_id = pedir_entero("\nIngresá el ID del producto a actualizar")

    try:
        with sqlite3.connect(NOMBRE_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (prod_id,))
            producto = cursor.fetchone()  # Busco un unico registro por ID

            if not producto:
                print(Fore.RED + f"✘ No se encontró ningún producto con el ID {prod_id}.")
                return

            # Desempaqueto los datos actuales del producto
            _, nombre_actual, desc_actual, cant_actual, precio_actual, cat_actual = producto

            print(
                Fore.YELLOW
                + f"\nModificando '{nombre_actual}' (ID {prod_id}). "
                + "Dejá en blanco y presioná Enter para mantener el valor actual."
            )

            # Pido los nuevos datos pasando el valor actual por si el usuario presiona Enter
            nuevo_nombre = pedir_texto("Nuevo nombre", obligatorio=True, valor_actual=nombre_actual)
            nueva_desc = pedir_texto(
                "Nueva descripción", obligatorio=False, valor_actual=desc_actual or ""
            )
            nueva_cant = pedir_entero("Nueva cantidad", valor_actual=cant_actual)
            nuevo_precio = pedir_decimal("Nuevo precio", valor_actual=precio_actual)
            nueva_cat = pedir_texto(
                "Nueva categoría", obligatorio=False, valor_actual=cat_actual or ""
            )

            # Actualizo el registro correspondiente a ese ID
            cursor.execute(
                """
                UPDATE productos
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
                """,
                (nuevo_nombre, nueva_desc, nueva_cant, nuevo_precio, nueva_cat, prod_id),
            )
            conn.commit()

        print(Fore.GREEN + "✔ Producto actualizado con éxito.")
    except sqlite3.Error as error:
        print(Fore.RED + f"✘ Error al actualizar el producto: {error}")


def eliminar_producto():
    """Busca un producto por ID y lo elimina previa confirmacion del usuario."""
    print(Fore.CYAN + Style.BRIGHT + "\n=== ELIMINAR PRODUCTO ===")
    visualizar_productos()  # Muestro el listado para verificar el ID antes de borrar

    prod_id = pedir_entero("\nIngresá el ID del producto a eliminar")

    try:
        with sqlite3.connect(NOMBRE_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE id = ?", (prod_id,))
            producto = cursor.fetchone()

            if not producto:
                print(Fore.RED + f"✘ No se encontró ningún producto con el ID {prod_id}.")
                return

            # Pido confirmacion explicita antes de borrar el registro
            confirmacion = (
                input(
                    Fore.YELLOW
                    + f"¿Seguro que querés eliminar '{producto[1]}' (ID {prod_id})? (s/n): "
                )
                .strip()
                .lower()
            )

            if confirmacion == "s":
                cursor.execute("DELETE FROM productos WHERE id = ?", (prod_id,))
                conn.commit()
                print(Fore.GREEN + "✔ Producto eliminado correctamente.")
            else:
                print(Fore.YELLOW + "! Operación cancelada.")
    except sqlite3.Error as error:
        print(Fore.RED + f"✘ Error al eliminar el producto: {error}")


def buscar_producto():
    """Permite buscar productos por ID, y de forma opcional por nombre o categoria."""
    print(Fore.CYAN + Style.BRIGHT + "\n=== BÚSQUEDA DE PRODUCTOS ===")
    print("1. Buscar por ID")
    print("2. Buscar por Nombre")
    print("3. Buscar por Categoría")

    opcion = input("Elegí una opción de búsqueda (1-3): ").strip()
    resultados = []

    try:
        with sqlite3.connect(NOMBRE_DB) as conn:
            cursor = conn.cursor()

            if opcion == "1":
                prod_id = pedir_entero("Ingresá el ID a buscar")
                cursor.execute("SELECT * FROM productos WHERE id = ?", (prod_id,))
                resultados = cursor.fetchall()
            elif opcion == "2":
                termino = pedir_texto("Ingresá el nombre (o parte del mismo)", obligatorio=True)
                # LIKE con '%' permite encontrar coincidencias parciales del nombre
                cursor.execute(
                    "SELECT * FROM productos WHERE nombre LIKE ? ORDER BY id ASC",
                    (f"%{termino}%",),
                )
                resultados = cursor.fetchall()
            elif opcion == "3":
                termino = pedir_texto("Ingresá la categoría", obligatorio=True)
                # LIKE con '%' permite buscar por categoria o parte del texto
                cursor.execute(
                    "SELECT * FROM productos WHERE categoria LIKE ? ORDER BY id ASC",
                    (f"%{termino}%",),
                )
                resultados = cursor.fetchall()
            else:
                print(Fore.RED + "✘ Opción de búsqueda no válida.")
                return
    except sqlite3.Error as error:
        print(Fore.RED + f"✘ Error en la búsqueda: {error}")
        return

    if not resultados:
        print(Fore.YELLOW + "! No se encontraron coincidencias.")
        return

    print(Fore.GREEN + f"\n✔ Resultados encontrados ({len(resultados)}):")
    for p in resultados:
        print(
            f"ID: {p[0]} | Nombre: {p[1]} | Desc: {p[2] or '-'} | Cant: {p[3]} | "
            f"Precio: ${p[4]:.2f} | Cat: {p[5] or 'Sin categoría'}"
        )


def reporte_bajo_stock():
    """Muestra productos con cantidad <= limite y resalta los que tienen stock 0 (agotados)."""
    print(Fore.CYAN + Style.BRIGHT + "\n=== REPORTE DE STOCK CRÍTICO ===")
    limite = pedir_entero("Ingresá el límite máximo de stock para el reporte")

    try:
        with sqlite3.connect(NOMBRE_DB) as conn:
            cursor = conn.cursor()
            # Filtro productos iguales o por debajo del limite, ordenados de menor a mayor stock
            cursor.execute(
                "SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC, id ASC",
                (limite,),
            )
            resultados = cursor.fetchall()
    except sqlite3.Error as error:
        print(Fore.RED + f"✘ Error al generar el reporte: {error}")
        return

    if not resultados:
        print(Fore.YELLOW + f"! No hay productos con cantidad menor o igual a {limite}.")
        return

    agotados = 0  # Contador para los productos que ya estan en 0 unidades
    print(Fore.YELLOW + f"\n! Productos con stock <= {limite} ({len(resultados)}):")
    for p in resultados:
        if p[3] == 0:
            agotados += 1
            # Resalto en rojo brillante los productos agotados para distinguirlos del resto
            print(
                Fore.RED
                + Style.BRIGHT
                + f"ID: {p[0]} | Nombre: {p[1]} | Stock: AGOTADO (0 u.) | "
                f"Precio: ${p[4]:.2f} | Categoría: {p[5] or 'Sin categoría'}"
            )
        else:
            print(
                Fore.YELLOW
                + f"ID: {p[0]} | Nombre: {p[1]} | Stock: {p[3]} u. | "
                f"Precio: ${p[4]:.2f} | Categoría: {p[5] or 'Sin categoría'}"
            )

    if agotados > 0:
        print(Fore.RED + f"\n✘ Atención: {agotados} producto(s) sin stock (agotados).")


def menu_principal():
    """Inicializa la base de datos y mantiene activo el menu en consola hasta salir."""
    inicializar_base_datos()  # Me aseguro de que exista la DB y la tabla al arrancar

    while True:
        print(Fore.MAGENTA + Style.BRIGHT + "\n========================================")
        print(Fore.MAGENTA + Style.BRIGHT + "     SISTEMA DE GESTIÓN DE INVENTARIO   ")
        print(Fore.MAGENTA + Style.BRIGHT + "========================================")
        print("1. Registrar nuevo producto")
        print("2. Visualizar productos registrados")
        print("3. Actualizar datos de un producto (por ID)")
        print("4. Eliminar un producto (por ID)")
        print("5. Buscar producto (por ID, Nombre o Categoría)")
        print("6. Reporte de stock crítico")
        print("7. Salir del programa")

        opcion = input(Fore.CYAN + "\nElegí una opción (1-7): ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            visualizar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print(Fore.CYAN + "\n¡Hasta luego! Saliendo del sistema de inventario.")
            break  # Corta el ciclo while y termina el programa
        else:
            print(Fore.RED + "✘ Opción inválida. Ingresá un número del 1 al 7.")


# Evita que menu_principal() se ejecute si este archivo se importa desde otro script
if __name__ == "__main__":
    menu_principal()