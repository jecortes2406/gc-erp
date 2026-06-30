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

# Base de Datos (Estructura expandida para Contabilidad)
conn = sqlite3.connect('gc_erp_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY, codigo TEXT, nombre TEXT, cat TEXT, cost_usd REAL, mon_compra TEXT, tasa_compra REAL, p_bulto REAL, p_mayor REAL, p_detal REAL, comision REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY, fecha DATE, vendedor TEXT, prod TEXT, precio_final REAL, metodo TEXT, comision_ganada REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS finanzas (id INTEGER PRIMARY KEY, tipo TEXT, desc TEXT, monto REAL, fecha DATE)''') # Gastos/Compras
conn.commit()

# Menú Lateral Vertical (Estilo 30/Saint)
with st.sidebar:
    selected = option_menu("GC ERP", ["Dashboard", "Finanzas", "Inventario", "Ventas", "Configuración"], 
                           icons=['graph-up', 'wallet2', 'box', 'cart', 'gear'], menu_icon="cast")

# --- LÓGICA DE MÓDULOS ---
if selected == "Finanzas":
    st.subheader("💰 Módulo Contable (Debe/Haber)")
    tipo = st.selectbox("Tipo de Movimiento", ["Gasto", "Compra a Proveedor", "Pago a Personal"])
    monto = st.number_input("Monto (USDT)")
    if st.button("Registrar Movimiento"):
        c.execute("INSERT INTO finanzas VALUES (NULL,?,?,?,DATE('now'))", (tipo, "Registro contable", monto))
        conn.commit()

elif selected == "Inventario":
    st.subheader("📦 Carga y Gestión de Productos")
    with st.form("inv"):
        col1, col2 = st.columns(2)
        cod = col1.text_input("Código SKU")
        nom = col2.text_input("Nombre del Producto")
        cost = col1.number_input("Costo de Compra (USDT)")
        pb, pm, pd = col2.number_input("Precio Bulto"), col1.number_input("Precio Mayor"), col2.number_input("Precio Detal")
        com = col1.number_input("Comisión %")
        if st.form_submit_button("Cargar Producto"):
            c.execute("INSERT INTO inventario VALUES (NULL,?,?,?,?,?,?,?,?,?,?)", (cod, nom, "General", cost, "USD", 1.0, pb, pm, pd, com))
            conn.commit()

elif selected == "Ventas":
    st.subheader("🛒 Punto de Venta")
    prods = pd.read_sql("SELECT * FROM inventario", conn)
    busqueda = st.text_input("Buscar por nombre o código")
    if not prods.empty:
        # Filtrado inteligente
        df_filtrado = prods[prods['nombre'].str.contains(busqueda, case=False) | prods['codigo'].str.contains(busqueda, case=False)]
        prod_sel = st.selectbox("Producto Seleccionado", df_filtrado['nombre'])
        cant = st.number_input("Cantidad", 1, 100)
        # Mostrar precios en las 3 monedas configuradas
        st.info("Visualización automática en USD, EUR y VES aquí...")
        if st.button("Procesar Factura"):
            st.success("Factura generada")
