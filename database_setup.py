import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# Crear tabla productos si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id TEXT PRIMARY KEY,
    nombre TEXT,
    cantidad INTEGER,
    precio REAL
)
""")

conn.commit()
conn.close()
print("Base de datos y tabla lista.")
