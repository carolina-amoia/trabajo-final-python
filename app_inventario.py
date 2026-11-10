import sqlite3


def inicializar_base_datos():
  """Crea la base de datos 'inventario.db' y la tabla 'productos'

  con sus respectivas columnas si no existen previamente.
  """
  conn = sqlite3.connect("inventario.db")
  cursor = conn.cursor()

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

  conn.commit()
  conn.close()


def registrar_producto():
  """Solicita los datos al usuario y registra un nuevo producto en la base de datos."""
  print("\n--- REGISTRAR NUEVO PRODUCTO ---")

  nombre = input("Ingrese el nombre del producto: ").strip()
  if not nombre:
    print("❌ Error: El nombre del producto no puede estar vacío.")
    return

  descripcion = input("Ingrese una breve descripción (opcional): ").strip()

  # Validación de entradas numéricas para evitar errores de tipo
  try:
    cantidad = int(input("Ingrese la cantidad disponible: "))
    precio = float(input("Ingrese el precio unitario: "))

    if cantidad < 0 or precio < 0:
      print("❌ Error: La cantidad y el precio no pueden ser negativos.")
      return
  except ValueError:
    print(
        "❌ Error: Debe ingresar valores numéricos válidos para la cantidad y"
        " el precio."
    )
    return

  categoria = input("Ingrese la categoría del producto (opcional): ").strip()

  # Inserción segura utilizando parámetros (?) para evitar inyecciones SQL
  conn = sqlite3.connect("inventario.db")
  cursor = conn.cursor()

  cursor.execute(
      """
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    """,
      (nombre, descripcion, cantidad, precio, categoria),
  )

  conn.commit()
  conn.close()
  print("¡Producto registrado con éxito!")


def visualizar_productos():
  """Consulta y muestra en formato de tabla todos los productos registrados."""
  conn = sqlite3.connect("inventario.db")
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM productos")
  productos = cursor.fetchall()
  conn.close()

  if not productos:
    print("\nℹ️ No hay productos registrados en el inventario.")
    return

  print("\n" + "=" * 80)
  print(
      f"{'ID':<4} | {'NOMBRE':<18} | {'DESCRIPCIÓN':<20} | {'CANT':<6} |"
      f" {'PRECIO':<10} | {'CATEGORÍA':<12}"
  )
  print("=" * 80)

  for p in productos:
    prod_id, nombre, desc, cant, precio, cat = p
    desc_corta = (desc[:18] + "..") if desc and len(desc) > 20 else (desc or "-")
    cat_texto = cat if cat else "Sin categoría"
    print(
        f"{prod_id:<4} | {nombre:<18} | {desc_corta:<20} | {cant:<6} |"
        f" ${precio:<9.2f} | {cat_texto:<12}"
    )
  print("=" * 80)


def actualizar_producto():
  """Actualiza los datos de un producto existente buscándolo por su ID."""
  visualizar_productos()

  try:
    prod_id = int(
        input(
            "\nIngrese el ID del producto que desea actualizar: "
        ).strip()
    )
  except ValueError:
    print("❌ Error: Debe ingresar un número entero válido para el ID.")
    return

  conn = sqlite3.connect("inventario.db")
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM productos WHERE id = ?", (prod_id,))
  producto = cursor.fetchone()

  if not producto:
    print(f"❌ No se encontró ningún producto con el ID {prod_id}.")
    conn.close()
    return

  print(
      f"\nModificando producto actual: '{producto[1]}'. Deje el campo en blanco y"
      " presione Enter para mantener el valor anterior."
  )

  nuevo_nombre = (
      input(f"Nuevo nombre [{producto[1]}]: ").strip() or producto[1]
  )
  nueva_desc = (
      input(f"Nueva descripción [{producto[2]}]: ").strip() or producto[2]
  )

  try:
    cant_input = input(f"Nueva cantidad [{producto[3]}]: ").strip()
    nueva_cant = int(cant_input) if cant_input else producto[3]

    precio_input = input(f"Nuevo precio [{producto[4]}]: ").strip()
    nuevo_precio = float(precio_input) if precio_input else producto[4]
  except ValueError:
    print("❌ Error: Los valores numéricos ingresados no son válidos.")
    conn.close()
    return

  nueva_cat = (
      input(f"Nueva categoría [{producto[5]}]: ").strip() or producto[5]
  )

  cursor.execute(
      """
        UPDATE productos
        SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
        WHERE id = ?
    """,
      (nuevo_nombre, nueva_desc, nueva_cant, nuevo_precio, nueva_cat, prod_id),
  )

  conn.commit()
  conn.close()
  print("¡Producto actualizado con éxito!")


def eliminar_producto():
  """Elimina un registro de la base de datos utilizando su ID."""
  visualizar_productos()

  try:
    prod_id = int(input("\nIngrese el ID del producto a eliminar: ").strip())
  except ValueError:
    print("❌ Error: ID inválido.")
    return

  conn = sqlite3.connect("inventario.db")
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM productos WHERE id = ?", (prod_id,))
  producto = cursor.fetchone()

  if not producto:
    print(f"❌ No se encontró ningún producto con el ID {prod_id}.")
    conn.close()
    return

  confirmacion = (
      input(
          f"¿Está seguro de eliminar el producto '{producto[1]}' (ID:"
          f" {prod_id})? (s/n): "
      )
      .strip()
      .lower()
  )

  if confirmacion == "s":
    cursor.execute("DELETE FROM productos WHERE id = ?", (prod_id,))
    conn.commit()
    print("¡Producto eliminado correctamente!")
  else:
    print("Operación cancelada.")

  conn.close()


def buscar_producto():
  """Permite buscar productos por ID, y opcionalmente por nombre o categoría."""
  print("\n--- BÚSQUEDA DE PRODUCTOS ---")
  print("1. Buscar por ID")
  print("2. Buscar por Nombre")
  print("3. Buscar por Categoría")

  opcion = input("Seleccione una opción de búsqueda (1-3): ").strip()

  conn = sqlite3.connect("inventario.db")
  cursor = conn.cursor()
  resultados = []

  if opcion == "1":
    try:
      prod_id = int(input("Ingrese el ID a buscar: ").strip())
      cursor.execute("SELECT * FROM productos WHERE id = ?", (prod_id,))
      resultados = cursor.fetchall()
    except ValueError:
      print("❌ Error: ID inválido.")
  elif opcion == "2":
    termino = input("Ingrese el nombre (o parte del mismo): ").strip()
    cursor.execute(
        "SELECT * FROM productos WHERE nombre LIKE ?", (f"%{termino}%",)
    )
    resultados = cursor.fetchall()
  elif opcion == "3":
    termino = input("Ingrese la categoría: ").strip()
    cursor.execute(
        "SELECT * FROM productos WHERE categoria LIKE ?", (f"%{termino}%",)
    )
    resultados = cursor.fetchall()
  else:
    print("❌ Opción no válida.")
    conn.close()
    return

  conn.close()

  if not resultados:
    print("\nℹ️ No se encontraron coincidencias.")
    return

  print(f"\n--- RESULTADOS DE BÚSQUEDA ({len(resultados)}) ---")
  for p in resultados:
    print(
        f"ID: {p[0]} | Nombre: {p[1]} | Desc: {p[2] or '-'} | Cant: {p[3]} |"
        f" Precio: ${p[4]:.2f} | Cat: {p[5] or 'Sin categoría'}"
    )


def reporte_bajo_stock():
  """Genera un reporte filtrando productos con cantidad menor o igual a un límite dado."""
  try:
    limite = int(
        input("\nIngrese el límite máximo de stock para el reporte: ").strip()
    )
  except ValueError:
    print("❌ Error: Debe ingresar un número entero.")
    return

  conn = sqlite3.connect("inventario.db")
  cursor = conn.cursor()

  cursor.execute(
      "SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC",
      (limite,),
  )
  resultados = cursor.fetchall()
  conn.close()

  if not resultados:
    print(f"\nℹ️ No hay productos con stock menor o igual a {limite}.")
    return

  print(f"\n--- REPORTE DE PRODUCTOS CON STOCK <= {limite} ---")
  for p in resultados:
    print(
        f"ID: {p[0]} | Nombre: {p[1]} | Stock: {p[3]} unidades | Precio:"
        f" ${p[4]:.2f} | Categoría: {p[5] or 'Sin categoría'}"
    )


def menu_principal():
  """Controla el bucle principal de la aplicación y despliega el menú en la terminal."""
  inicializar_base_datos()

  while True:
    print("\n========================================")
    print("    SISTEMA DE GESTIÓN DE INVENTARIO    ")
    print("========================================")
    print("1. Registrar nuevo producto")
    print("2. Visualizar productos registrados")
    print("3. Actualizar datos de un producto (por ID)")
    print("4. Eliminar un producto (por ID)")
    print("5. Buscar producto (por ID, Nombre o Categoría)")
    print("6. Reporte de stock crítico")
    print("7. Salir del programa")

    opcion = input("\nSeleccione una opción (1-7): ").strip()

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
      print("\nSaliendo del sistema de inventario. ¡Hasta luego!")
      break
    else:
      print("❌ Opción inválida. Por favor, ingrese un número del 1 al 7.")


# Punto de entrada principal del script
if __name__ == "__main__":
  menu_principal()