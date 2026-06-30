import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="GC ERP Profesional")

# --- CSS PERSONALIZADO (ROJO CARMESÍ Y COBRE) ---
st.markdown("""
    <style>
    .stApp {background-color: #fcfcfc;}
    section[data-testid="stSidebar"] {background-color: #fdf5f5; border-right: 2px solid #CD7F32;}
    .css-1r6slb0 {color: #990000;}
    div.stButton > button {background-color: #CD7F32; color: white; border-radius: 5px; width: 100%;}
    div.stMetric {background-color: #ffffff; padding: 10px; border-left: 5px solid #990000;}
    </style>
    """, unsafe_allow_html=True)

# Inicializar BD
conn = sqlite3.connect('gc_erp_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, nombre TEXT, foto TEXT, p_detal REAL, p_mayor REAL, p_bulto REAL)''')
conn.commit()

# --- NAVEGACIÓN LATERAL ---
with st.sidebar:
    st.image("logo.png") # Asegúrate de tener este logo
    selected = option_menu("GC ERP", ["Nueva Venta", "Inventario", "Reportes", "Configuración"], icons=['cart', 'box', 'graph-up', 'gear'])

# --- MÓDULO DE VENTAS (REPLICA DE 425.jpg) ---
if selected == "Nueva Venta":
    col_centro, col_der = st.columns([2, 1])
    
    with col_centro:
        st.subheader("🛒 Catálogo de Productos")
        busqueda = st.text_input("🔍 Buscar producto...")
        items = pd.read_sql("SELECT * FROM items", conn)
        
        # Grid de productos (Tarjetas)
        cols = st.columns(3)
        for i, row in items.iterrows():
            with cols[i % 3]:
                st.markdown(f"**{row['nombre']}**")
                st.write(f"💵 ${row['p_detal']}")
                if st.button(f"Agregar", key=f"add_{i}"):
                    st.session_state.canasta = row
                    
    with col_der:
        st.subheader("🧺 Canasta")
        if 'canasta' in st.session_state:
            item = st.session_state.canasta
            st.write(f"**{item['nombre']}**")
            st.write(f"Total: ${item['p_detal']}")
            if st.button("Confirmar Pedido"):
                st.success("Venta procesada.")
        else:
            st.info("La canasta está vacía")

# --- MÓDULO DE INVENTARIO ---
elif selected == "Inventario":
    st.subheader("📦 Carga de Inventario")
    with st.form("carga"):
        nombre = st.text_input("Nombre")
        p_d = st.number_input("Precio Detal")
        p_m = st.number_input("Precio Mayor")
        p_b = st.number_input("Precio Bulto")
        if st.form_submit_button("Guardar"):
            c.execute("INSERT INTO items (nombre, p_detal, p_mayor, p_bulto) VALUES (?,?,?,?)", (nombre, p_d, p_m, p_b))
            conn.commit()
            st.rerun()
