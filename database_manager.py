# --- AÑADIR A TU DATABASE_MANAGER.PY (SI NO ESTÁ) ---
def obtener_todos_productos():
    conn = sqlite3.connect('gc_erp.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    data = c.fetchall()
    conn.close()
    return data
