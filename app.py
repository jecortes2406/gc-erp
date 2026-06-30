import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu

# Configuración Estética
st.set_page_config(page_title="GC ERP Pro", layout="wide")
st.markdown("""<style>
    [data-testid="stSidebar"] {background-color: #fdf5f5;}
    .nav-link {color: #990000 !important;}
    .nav-link-selected {background-color: #CD7F32 !important; color: white !important;}
    </style>""", unsafe_allow_html=True)

# Base de Datos
conn = sqlite3.connect('gc_erp_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY, nombre TEXT, cat TEXT, cost REAL, p_bulto REAL, p_mayor REAL, p_detal REAL, comision REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY, fecha DATE, vendedor TEXT, producto TEXT, precio_final REAL, metodo TEXT, comision_ganada REAL)''')
conn.commit()

# Menú
with st.sidebar:
    selected = option_menu("GC ERP", ["Dashboard", "Inventario", "Ventas"], icons=['graph-up', 'box', 'cart'])

if selected == "Inventario":
    st.subheader("📦 Carga de Inventario")
    with st.form("carga"):
        nombre = st.text_input("Producto")
        cat = st.text_input("Categoría")
        cost = st.number_input("Costo de Compra (USDT)")
        pb = st.number_input("Precio Bulto")
        pm = st.number_input("Precio Mayor")
        pd = st.number_input("Precio Detal")
        com = st.number_input("Comisión Vendedor (%)")
        if st.form_submit_button("Guardar Producto"):
            c.execute("INSERT INTO inventario VALUES (NULL,?,?,?,?,?,?,?)", (nombre,cat,cost,pb,pm,pd,com))
            conn.commit()
            st.success("Producto guardado")

elif selected == "Ventas":
    st.subheader("🛒 Facturación")
    prods = pd.read_sql("SELECT * FROM inventario", conn)
    if not prods.empty:
        prod_sel = st.selectbox("Producto", prods['nombre'])
        tipo_precio = st.radio("Seleccionar Tipo de Precio", ["Bulto", "Mayor", "Detal"])
        vendedor = st.text_input("Vendedor")
        metodo = st.selectbox("Pago", ["Efectivo USD", "Efectivo VES", "Pago Móvil"])
        
        # Obtener valores
        p = prods[prods['nombre'] == prod_sel].iloc[0]
        precio_vta = p['p_bulto'] if tipo_precio == "Bulto" else (p['p_mayor'] if tipo_precio == "Mayor" else p['p_detal'])
        com_pct = p['comision']
        
        st.write(f"### Precio a cobrar: {precio_vta} USDT")
        if st.button("Procesar Venta"):
            com_ganada = precio_vta * (com_pct/100)
            c.execute("INSERT INTO ventas VALUES (NULL, DATE('now'),?,?,?,?,?)", (vendedor, prod_sel, precio_vta, metodo, com_ganada))
            conn.commit()
            st.success("Venta procesada")
    else: st.warning("Cargue productos primero")

elif selected == "Dashboard":
    st.title("📈 Métricas")
    df = pd.read_sql("SELECT * FROM ventas", conn)
    if not df.empty:
        st.metric("Venta Total", f"{df['precio_final'].sum()} USDT")
        st.bar_chart(df.groupby('producto')['precio_final'].sum())
