import streamlit as st
import pandas as pd
from modulo_inventario import render_modulo_inventario

# 1. CONFIGURACIÓN
st.set_page_config(page_title="GC Grupo Comercial C.A. - ERP", page_icon="💼", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #002366; } 
    h1, h2, h3, p, div { color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE TASAS PERSISTENTES (Sin valores fijos precargados)
if 'tasa_binance' not in st.session_state:
    st.session_state.tasa_binance = 0.00
if 'tasa_bcv' not in st.session_state:
    st.session_state.tasa_bcv = 0.00

st.sidebar.markdown("## ⚜️ GC - Grupo Comercial C.A.")
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Control de Tasas (Manual)")

# Tasas editables - EL ADMIN LAS COLOCA Y SE QUEDAN GUARDADAS
st.session_state.tasa_binance = st.sidebar.number_input("Tasa Binance (P2P)", value=st.session_state.tasa_binance, format="%.2f")
st.session_state.tasa_bcv = st.sidebar.number_input("Tasa BCV", value=st.session_state.tasa_bcv, format="%.2f")

# 3. NAVEGACIÓN
modulos = ["📊 Dashboard", "🗂️ Gestión / Inventario", "🧾 POS", "🛒 Compras", "📈 Reportes"]
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos)

# 4. DISTRIBUCIÓN
if modulo_seleccionado == "📊 Dashboard":
    st.title("Panel de Control Ejecutivo")
    # Aquí irá el dashboard que construiremos mañana
elif modulo_seleccionado == "🗂️ Gestión / Inventario":
    render_modulo_inventario()
else:
    st.title(modulo_seleccionado)
