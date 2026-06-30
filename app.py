import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu

# --- ESTRUCTURA DE DATOS TIPO ERP-NEXT ---
def init_db():
    conn = sqlite3.connect('gc_erp_pro.db', check_same_thread=False)
    c = conn.cursor()
    # Tabla Maestro de Productos (Estructura profesional)
    c.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY, sku TEXT, nombre TEXT, categoria TEXT, 
        costo_usd REAL, p_detal REAL, p_mayor REAL, p_bulto REAL, comision REAL)''')
    # Tabla de Ventas con Logística
    c.execute('''CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY, fecha DATE, cliente TEXT, tipo_entrega TEXT, 
        subtotal REAL, delivery_cost REAL, total REAL, metodo_pago TEXT)''')
    conn.commit()
    return conn

# --- INTERFAZ VISUAL ---
st.set_page_config(layout="wide")
conn = init_db()

with st.sidebar:
    selected = option_menu("GC ERP Pro", ["Dashboard", "Inventario", "Ventas", "Logística", "Configuración"])

if selected == "Inventario":
    st.subheader("📦 Catálogo de Productos (Estilo ERPNext)")
    with st.form("carga_item"):
        c1, c2 = st.columns(2)
        sku = c1.text_input("SKU/Código")
        nombre = c2.text_input("Nombre del Producto")
        costo = c1.number_input("Costo de Compra (USD)")
        precios = [c2.number_input("Precio Detal"), c1.number_input("Precio Mayor"), c2.number_input("Precio Bulto")]
        comision = c1.number_input("Comisión %")
        if st.form_submit_button("Guardar en Catálogo"):
            conn.cursor().execute("INSERT INTO items VALUES (NULL,?,?,?,?,?,?,?,?)", (sku, nombre, "General", costo, *precios, comision))
            conn.commit()
            st.success("Item registrado.")

elif selected == "Ventas":
    st.subheader("🛒 Punto de Venta (POS)")
    items = pd.read_sql("SELECT * FROM items", conn)
    # Lógica de Carrito aquí...
    st.dataframe(items, use_container_width=True)

elif selected == "Logística":
    st.subheader("🚚 Gestión de Entregas (Pick-up / Delivery)")
    # Aquí incorporamos la lógica de costo adicional y zonas
