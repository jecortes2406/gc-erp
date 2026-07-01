import streamlit as st
import pandas as pd

# Importación de módulos locales
from modulo_inventario import render_modulo_inventario
from modulo_pos import render_modulo_pos
from modulo_contable import render_modulo_contable

# 1. CONFIGURACIÓN GLOBAL
st.set_page_config(page_title="GC Grupo Comercial C.A. - ERP", page_icon="💼", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #002366; } 
    h1, h2, h3, p, div { color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE TASAS PERSISTENTES
if 'tasa_binance' not in st.session_state:
    st.session_state.tasa_binance = 0.00
if 'tasa_bcv' not in st.session_state:
    st.session_state.tasa_bcv = 0.00

# Barra Lateral
st.sidebar.markdown("## ⚜️ GC - Grupo Comercial C.A.")
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Control de Tasas (Manual)")

st.session_state.tasa_binance = st.sidebar.number_input("Tasa Binance (P2P)", value=st.session_state.tasa_binance, format="%.2f")
st.session_state.tasa_bcv = st.sidebar.number_input("Tasa BCV", value=st.session_state.tasa_bcv, format="%.2f")

# 3. MENÚ DE NAVEGACIÓN
modulos = ["📊 Dashboard", "🗂️ Gestión / Inventario", "🧾 POS", "🛒 Compras", "📈 Reportes"]
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos)

# 4. DISTRIBUCIÓN DE MÓDULOS
if modulo_seleccionado == "📊 Dashboard":
    from dashboard import render_dashboard
    render_dashboard()
    
elif modulo_seleccionado == "🗂️ Gestión / Inventario":
    render_modulo_inventario()
    
elif modulo_seleccionado == "🧾 POS":
    render_modulo_pos()

elif modulo_seleccionado == "🛒 Compras":
    render_modulo_contable()

elif modulo_seleccionado == "📈 Reportes":
    st.subheader("📈 Reportes Generales")
    st.info("Módulo de reportes financieros en fase de conexión con base de datos.")
