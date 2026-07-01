import streamlit as st
import pandas as pd
import urllib.request
import json
from modulo_inventario import render_modulo_inventario
import utils 

# 1. CONFIGURACIÓN INICIAL (DEBE SER LO PRIMERO)
st.set_page_config(page_title="GC Grupo Comercial C.A. - ERP", page_icon="💼", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #002366; } 
    .card-white { background-color: #003399; padding: 20px; border-radius: 14px; border: 1px solid #B87333; }
    h1, h2, h3, p, div { color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# 2. LÓGICA DE TASAS (Integrada)
if 'tasa_binance' not in st.session_state:
    st.session_state.tasa_binance, st.session_state.tasa_bcv = utils.obtener_tasas()

# Barra lateral de control
st.sidebar.markdown("## ⚜️ GC - Grupo Comercial C.A.")
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Control de Tasas (Master)")
st.session_state.tasa_binance = st.sidebar.number_input("Tasa Binance (P2P)", value=st.session_state.tasa_binance, format="%.2f")
st.session_state.tasa_bcv = st.sidebar.number_input("Tasa BCV", value=st.session_state.tasa_bcv, format="%.2f")
st.session_state.referencia_master = st.session_state.tasa_binance

# 3. MENÚ DE NAVEGACIÓN
modulos = [
    "📊 Panel Principal / Dashboard", "🗂️ Gestión / Inventario", "🧾 Crear Factura (POS)", 
    "🛒 Compras a Proveedores", "📈 Reportes Generales"
]
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos)

# 4. DISTRIBUCIÓN DE MÓDULOS
if modulo_seleccionado == "📊 Panel Principal / Dashboard":
    st.title("Bienvenido al Dashboard")
    
elif modulo_seleccionado == "🗂️ Gestión / Inventario":
    render_modulo_inventario()

else:
    st.title(modulo_seleccionado)
    st.info("Módulo en desarrollo.")
