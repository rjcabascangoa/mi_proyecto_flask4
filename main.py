# main.py

import sqlite3

# ================================
# Clase Producto
# ================================
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"[{self.id}] {self.nombre} - Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"

# ================================
# Clase Inventario
# ================================
class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario: id -> Producto
        self.conn = sqlite3.connect("inventario.db")
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    # Crear tabla en SQLite
    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
        """)
        self.conn.commit()

    # -------------------------------
    # CRUD
    # -------------------------------
    def agregar_producto(self, producto):
        if producto.id in self.productos:
            print("El producto ya existe en el inventario.")
            return
        self.productos[producto.id] = producto
        self.cursor.execute(
            "INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
            (producto.id, producto.nombre, producto.cantidad, producto.precio)
        )
        self.conn.commit()
        print(f"Producto '{producto.nombre}' agregado.")

    def eliminar_producto(self, id):
        if id in self.productos:
            nombre = self.productos[id].nombre
            del self.productos[id]
            self.cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
            self.conn.commit()
            print(f"Producto '{nombre}' eliminado.")
        else:
            print("Producto no encontrado.")

    def actualizar_producto(self, id, cantidad=None, precio=None):
        if id in self.productos:
            if cantidad is not None:
                self.productos[id].cantidad = cantidad
            if precio is not None:
                self.productos[id].precio = precio
            self.cursor.execute(
                "UPDATE productos SET cantidad=?, precio=? WHERE id=?",
                (self.productos[id].cantidad, self.productos[id].precio, id)
            )
            self.conn.commit()
            print(f"Producto '{self.productos[id].nombre}' actualizado.")
        else:
            print("Producto no encontrado.")

    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        if resultados:
            for p in resultados:
                print(p)
        else:
            print("No se encontraron productos.")

    def mostrar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
            return
        for producto in self.productos.values():
            print(producto)

    def cargar_desde_db(self):
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()
        for row in rows:
            id, nombre, cantidad, precio = row
            self.productos[id] = Producto(id, nombre, cantidad, precio)

# ================================
# Menú interactivo
# ================================
def menu():
    inventario = Inventario()
    inventario.cargar_desde_db()

    while True:
        print("\n=== SISTEMA DE INVENTARIO ===")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar inventario")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            id = input("ID: ")
            nombre = input("Nombre: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            inventario.agregar_producto(Producto(id, nombre, cantidad, precio))

        elif opcion == "2":
            id = input("ID del producto a eliminar: ")
            inventario.eliminar_producto(id)

        elif opcion == "3":
            id = input("ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (dejar vacío si no cambia): ")
            precio = input("Nuevo precio (dejar vacío si no cambia): ")
            cantidad = int(cantidad) if cantidad else None
            precio = float(precio) if precio else None
            inventario.actualizar_producto(id, cantidad, precio)

        elif opcion == "4":
            nombre = input("Nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_productos()

        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")

# ================================
# Ejecutar programa
# ================================
if __name__ == "__main__":
    menu()
