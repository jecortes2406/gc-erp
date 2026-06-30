import sqlite3
def init_db():
    conn = sqlite3.connect('erp_maestro.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS productos 
                 (id INTEGER PRIMARY KEY, sku TEXT, nombre TEXT, 
                  costo REAL, moneda TEXT, stock INTEGER, 
                  margen_d REAL, margen_b REAL, margen_m REAL, 
                  iva REAL, vendedor TEXT)''')
    conn.commit()
    conn.close()
