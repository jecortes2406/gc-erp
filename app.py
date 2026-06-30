import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu
import os

# Configuración Visual
st.set_page_config(page_title="GC ERP Pro", layout="wide")
st.markdown("""<style>
    [data-testid="stSidebar"] {background-color: #fdf5f5;}
    .nav-link {color: #990000 !important;}
    .nav-link-selected {background-color: #CD7F32 !important; color: white !important;}
    </style>""", unsafe_allow_html=True)

# Base de Datos (Estructura expandida para Multimedia)
conn = sqlite3.connect('gc_erp_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS config_empresa (id INTEGER PRIMARY KEY, nombre TEXT, logo_path TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY, codigo TEXT, nombre TEXT, foto_path TEXT, p_detal REAL, comision REAL)''')
conn.commit()

# --- MÓDULOS DE CONFIGURACIÓN DE IDENTIDAD ---
with st.sidebar:
    selected = option_menu("GC ERP", ["Dashboard", "Configuración Empresa", "Inventario", "Ventas"])

if selected == "Configuración Empresa":
    st.subheader("🏢 Datos de la Empresa")
    nombre_empresa = st.text_input("Nombre de la Empresa")
    logo_file = st.file_uploader("Cargar Logo de Empresa", type=['png', 'jpg'])
    
    if logo_file and st.button("Guardar Identidad"):
        # Guardar imagen en disco
        with open("logo.png", "wb") as f:
            f.write(logo_file.getbuffer())
        c.execute("INSERT OR REPLACE INTO config_empresa VALUES (1, ?, ?)", (nombre_empresa, "logo.png"))
        conn.commit()
        st.success("Logo y datos actualizados.")

elif selected == "Inventario":
    st.subheader("📦 Carga de Producto con Imagen")
    with st.form("carga_producto"):
        nombre = st.text_input("Nombre del Producto")
        foto = st.file_uploader("Foto del Producto", type=['jpg', 'png'])
        precio = st.number_input("Precio Detal")
        
        if st.form_submit_button("Guardar"):
            path = f"img_{nombre}.jpg"
            if foto:
                with open(path, "wb") as f:
                    f.write(foto.getbuffer())
            c.execute("INSERT INTO inventario (nombre, foto_path, p_detal) VALUES (?,?,?)", (nombre, path, precio))
            conn.commit()
            st.success("Producto y foto guardados.")

elif selected == "Ventas":
    st.subheader("🛒 Punto de Venta Visual")
    prods = pd.read_sql("SELECT * FROM inventario", conn)
    for index, row in prods.iterrows():
        col1, col2 = st.columns([1, 3])
        if os.path.exists(row['foto_path']):
            col1.image(row['foto_path'], width=100)
        col2.write(f"**{row['nombre']}** - Precio: {row['p_detal']} USD")
        if col2.button(f"Vender {row['nombre']}", key=row['id']):
            st.write("Procesando...")
