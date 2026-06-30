import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu

# Configuración Estética (Rojo Carmesí y Bronce)
st.set_page_config(page_title="GC ERP Pro", layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebar"] {background-color: #fdf5f5;}
    .nav-link {color: #990000 !important;}
    .nav-link-selected {background-color: #CD7F32 !important; color: white !important;}
    </style>
""", unsafe_allow_html=True)

# Módulo de Navegación Lateral (Interfaz tipo App)
with st.sidebar:
    selected = option_menu("GC ERP", ["Inicio", "Inventario", "Ventas", "Dashboard", "Cuentas"],
                           icons=['house', 'box', 'cart', 'graph-up', 'list-task'], menu_icon="cast")

# Lógica del Dashboard con KPIs de Margen
if selected == "Dashboard":
    st.title("📊 Análisis de Rendimiento")
    conn = sqlite3.connect('gc_erp_pro.db')
    df_ventas = pd.read_sql("SELECT * FROM ventas", conn)
    
    if not df_ventas.empty:
        col1, col2, col3 = st.columns(3)
        # KPI: Más vendido
        top_prod = df_ventas.groupby('producto')['monto_usdt'].sum().idxmax()
        # KPI: Menos vendido
        low_prod = df_ventas.groupby('producto')['monto_usdt'].sum().idxmin()
        
        col1.metric("Producto Estrella", top_prod)
        col2.metric("Rotación Baja", low_prod)
        st.bar_chart(df_ventas.groupby('producto')['monto_usdt'].sum())
    else:
        st.info("Sin datos para procesar métricas.")

elif selected == "Inventario":
    # Aquí iría tu carga con precio de compra, moneda y categoría
    st.subheader("📦 Control de Stock")
    # ... (estructura de carga con categorías y costos)
