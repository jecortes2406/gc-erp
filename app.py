import streamlit as st
import sqlite3
import pandas as pd

# Inicializar Base de Datos
conn = sqlite3.connect('gc_erp_pro.db', check_same_thread=False)
c = conn.cursor()
# Tabla de Inventario con categorías y comisión específica por producto
c.execute('''CREATE TABLE IF NOT EXISTS inventario 
             (id INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, p_bulto REAL, p_mayor REAL, p_detal REAL, comision_pct REAL)''')
# Tabla de Ventas con detalle de método de pago
c.execute('''CREATE TABLE IF NOT EXISTS ventas 
             (id INTEGER PRIMARY KEY, fecha DATE, vendedor TEXT, producto TEXT, metodo_pago TEXT, monto_usdt REAL, comision_ganada REAL)''')
conn.commit()

# --- INTERFAZ ---
st.title("🚀 GC ERP Enterprise")
menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Inventario y Carga", "Ventas", "Comisiones"])

if menu == "Inventario y Carga":
    st.subheader("Carga Profesional de Inventario")
    col1, col2 = st.columns(2)
    nombre = col1.text_input("Nombre del Producto")
    cat = col2.text_input("Categoría")
    b = col1.number_input("Precio Bulto")
    m = col2.number_input("Precio Mayor")
    d = col1.number_input("Precio Detal")
    com = col2.number_input("Comisión % por Producto")
    
    if st.button("Registrar Producto"):
        c.execute("INSERT INTO inventario (nombre, categoria, p_bulto, p_mayor, p_detal, comision_pct) VALUES (?,?,?,?,?,?)", (nombre, cat, b, m, d, com))
        conn.commit()
