import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de página con colores institucionales
st.set_page_config(page_title="GC Grupo Comercial - Admin", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #002366; color: #FFFFFF; }
    h1, h2, h3 { color: #CD7F32; }
    </style>
""", unsafe_allow_html=True)

# Lógica de Blindaje Cambiario
def calcular_precios(costo_usd, margen_pct, tasa_bcv, tasa_binance):
    precio_base_usd = costo_usd * (1 + margen_pct / 100)
    return {
        "detal_ves": precio_base_usd * tasa_bcv,
        "mayor_ves": (precio_base_usd * 0.90) * tasa_bcv, # Ejemplo descuento mayor
        "blindaje_referencia": precio_base_usd * tasa_binance
    }

# --- Sidebar para Control de Tasas ---
st.sidebar.title("GC Grupo Comercial")
tasa_bcv = st.sidebar.number_input("Tasa BCV (VES/USD)", value=36.50)
tasa_euro = st.sidebar.number_input("Tasa Euro BCV", value=40.00)
tasa_binance = st.sidebar.number_input("Tasa Binance (Ref)", value=37.00)

# --- Módulo de KPIs (Mediciones de Vendedores) ---
def render_kpi_dashboard():
    st.header("📈 Dashboard de Gestión y KPIs")
    # KPIs típicos: Ventas totales, Tasa de Conversión, Ticket Promedio, Margen por vendedor
    data = {'Vendedor': ['Vendedor A', 'Vendedor B', 'Vendedor C'],
            'Ventas': [1500, 2200, 1800],
            'Conversión': [0.75, 0.85, 0.60]}
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Vendedor', y='Ventas', title="Rendimiento por Vendedor")
    st.plotly_chart(fig)

# --- Módulo de Inventario Inteligente (Huesos y Top Ventas) ---
def render_inventario_analisis():
    st.subheader("📦 Análisis de Inventario")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("🔥 Top 10 Más Vendidos")
        # Aquí iría el query a tu DB
    with col2:
        st.write("💰 Mayor Margen")
    with col3:
        st.write("🦴 Productos Hueso (Promociones)")
        # Botón para crear promoción en este producto
        if st.button("Crear Promo Hueso"):
            st.info("Configurando descuento automático...")

# Menú principal
menu = st.sidebar.radio("Navegación", ["Dashboard", "Inventario", "Facturación", "Gastos"])

if menu == "Dashboard":
    render_kpi_dashboard()
elif menu == "Inventario":
    render_inventario_analisis()
