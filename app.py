from flask import Flask, render_template, request, redirect, url_for
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

# ================================
# Clase Inventario
# ================================
class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario: id -> Producto
        self.conn = sqlite3.connect("inventario.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.crear_tabla()
        self.cargar_desde_db()

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

    def agregar_producto(self, producto):
        self.productos[producto.id] = producto
        self.cursor.execute(
            "INSERT OR REPLACE INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
            (producto.id, producto.nombre, producto.cantidad, producto.precio)
        )
        self.conn.commit()

    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]
        self.cursor.execute("DELETE FROM productos WHERE id=?", (id,))
        self.conn.commit()

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

    def cargar_desde_db(self):
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()
        for row in rows:
            id, nombre, cantidad, precio = row
            self.productos[id] = Producto(id, nombre, cantidad, precio)

# ================================
# Inicializar Flask
# ================================
app = Flask(__name__)
inv = Inventario()

# ================================
# Rutas Flask
# ================================

@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/inventario')
def inventario():
    return render_template('inventario.html', productos=list(inv.productos.values()))

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    id = request.form['id']
    nombre = request.form['nombre']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    nuevo = Producto(id, nombre, cantidad, precio)
    inv.agregar_producto(nuevo)
    return redirect(url_for('inventario'))

@app.route('/eliminar_producto/<id>', methods=['POST'])
def eliminar_producto(id):
    inv.eliminar_producto(id)
    return redirect(url_for('inventario'))

@app.route('/actualizar_producto/<id>', methods=['POST'])
def actualizar_producto(id):
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])
    inv.actualizar_producto(id, cantidad, precio)
    return redirect(url_for('inventario'))

@app.route('/about')
def about():
    return render_template('about.html', title='Acerca de')

@app.route('/contactos')
def contactos():
    return render_template('contactos.html', title='Contactos')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

# ================================
# Ejecutar aplicación
# ================================
if __name__ == '__main__':
    app.run(debug=True)
