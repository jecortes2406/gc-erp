import sqlite3

def init_db():
    conn = sqlite3.connect('gc_erp.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nombre TEXT, sku TEXT, costo_usd REAL, 
                  precio_detal REAL, precio_mayor REAL, stock INTEGER)''')
    conn.commit()
    conn.close()

def insertar_producto(nombre, sku, costo, p_detal, p_mayor, stock):
    conn = sqlite3.connect('gc_erp.db')
    c = conn.cursor()
    c.execute("INSERT INTO productos (nombre, sku, costo_usd, precio_detal, precio_mayor, stock) VALUES (?, ?, ?, ?, ?, ?)",
              (nombre, sku, costo, p_detal, p_mayor, stock))
    conn.commit()
    conn.close()

def obtener_todos_productos():
    conn = sqlite3.connect('gc_erp.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    data = c.fetchall()
    conn.close()
    return data
