# --- AÑADIR A TU DATABASE_MANAGER.PY (SI NO ESTÁ) ---
def obtener_todos_productos():
    conn = sqlite3.connect('gc_erp.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    data = c.fetchall()
    conn.close()
    return data
def actualizar_stock(producto_id, cantidad_vendida):
    conn = sqlite3.connect('gc_erp.db')
    c = conn.cursor()
    # Restamos el stock actual menos lo vendido
    c.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad_vendida, producto_id))
    conn.commit()
    conn.close()
