import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu
import os

# Configuración Visual
st.set_page_config(page_title="GC ERP Pro", layout="wide")
st.markdown("""<style>
    .stApp {background-color: #fcfcfc;}
    section[data-testid="stSidebar"] {background-color: #fdf5f5; border-right: 2px solid #CD7F32;}
    .nav-link {color: #990000 !important;}
    .nav-link-selected {background-color: #CD7F32 !important; color: white !important;}
    div.stButton > button {background-color: #CD7F32; color: white; border-radius: 5px;}
    </style>""", unsafe_allow_html=True)

# Base de Datos
conn = sqlite3.connect('gc_erp_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, nombre TEXT, p_detal REAL, p_mayor REAL, p_bulto REAL, foto TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY, fecha DATE, prod TEXT, total REAL)''')
conn.commit()

# Menú Lateral
with st.sidebar:
    selected = option_menu("GC ERP", ["Nueva Venta", "Inventario", "Dashboard"], icons=['cart', 'box', 'graph-up'])

# Módulo de Ventas (Punto de Venta)
if selected == "Nueva Venta":
    st.subheader("🛒 Punto de Venta")
    items = pd.read_sql("SELECT * FROM items", conn)
    
    col_centro, col_der = st.columns([2, 1])
    with col_centro:
        for i, row in items.iterrows():
            st.write(f"**{row['nombre']}** - ${row['p_detal']}")
            if st.button(f"Agregar {row['nombre']}", key=f"btn_{i}"):
                st.session_state.cart = row
    
    with col_der:
        st.subheader("🧺 Canasta")
        if 'cart' in st.session_state:
            st.write(f"Producto: {st.session_state.cart['nombre']}")
            st.write(f"Total: ${st.session_state.cart['p_detal']}")
            if st.button("Confirmar Venta"):
                c.execute("INSERT INTO ventas (fecha, prod, total) VALUES (DATE('now'),?,?)", 
                          (st.session_state.cart['nombre'], st.session_state.cart['p_detal']))
                conn.commit()
                st.success("Venta procesada!")
        else:
            st.info("Canasta vacía")

# Módulo Inventario
elif selected == "Inventario":
    st.subheader("📦 Carga de Inventario")
    with st.form("carga"):
        nom = st.text_input("Nombre")
        p_d = st.number_input("Precio Detal")
        p_m = st.number_input("Precio Mayor")
        p_b = st.number_input("Precio Bulto")
        if st.form_submit_button("Guardar"):
            c.execute("INSERT INTO items (nombre, p_detal, p_mayor, p_bulto) VALUES (?,?,?,?)", (nom, p_d, p_m, p_b))
            conn.commit()
            st.rerun()

elif selected == "Dashboard":
    st.title("📈 Métricas Gerenciales")
    df = pd.read_sql("SELECT * FROM ventas", conn)
    if not df.empty:
        st.bar_chart(df.groupby('prod')['total'].sum())
