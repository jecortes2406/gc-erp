import streamlit as st
import pandas as pd
import urllib.request
import json

from database_manager import init_db
from modulo_inventario import mostrar_formulario_inventario

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="GC Grupo Comercial C.A. - ERP",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)
init_db()

# Inicialización de estado
if 'empresa' not in st.session_state: st.session_state.empresa = "Grupo Comercial C.A."
if 'tasa_binance' not in st.session_state: st.session_state.tasa_binance = 46.50
if 'tasa_bcb_usd' not in st.session_state: st.session_state.tasa_bcb_usd = 42.35
if 'tasa_bcb_eur' not in st.session_state: st.session_state.tasa_bcb_eur = 45.20

# =====================================================================
# 2. ESTILOS CSS (Sin cambios)
# =====================================================================
st.markdown("""<style>
    .stApp { background-color: #F8FAFC; }
    .card-white { background-color: #FFFFFF; padding: 20px; border-radius: 14px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 15px; border: 1px solid #E2E8F0; }
    .card-dark { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #FFFFFF; padding: 25px; border-radius: 14px; margin-bottom: 15px; }
    .card-title { font-size: 13px; font-weight: 700; color: #64748B; text-transform: uppercase; }
    .card-value { font-size: 28px; font-weight: 700; color: #1E293B; }
    .welcome-title { font-size: 28px; font-weight: 700; color: #0F172A; }
    </style>""", unsafe_allow_html=True)

# =====================================================================
# 3. PANEL IZQUIERDO Y NAVEGACIÓN
# =====================================================================
st.sidebar.markdown("## ⚜️ GC")
st.sidebar.markdown(f"### {st.session_state.empresa}")
st.sidebar.markdown("---")

# Tasas
if st.sidebar.button("🔄 Actualizar Tasas BCV"): st.rerun()

st.session_state.tasa_binance = st.sidebar.number_input(
    "Tasa Binance P2P (Manual):", min_value=0.0, value=st.session_state.tasa_binance, step=0.1, key="tasa_binance"
)

# MENÚ DE OPERACIONES (CORREGIDO)
modulos = [
    "📊 Panel Principal / Dashboard", "📦 Órdenes Online", "🧾 Crear Factura (POS)", 
    "📑 Facturas Emitidas", "📝 Cotizaciones", "💰 Control de Cajas", 
    "📉 Flujo de Caja", "👥 Cuentas x Cobrar", "🛒 Compras a Proveedores", 
    "🗂️ Gestión / Inventario", "📈 Reportes Generales", "⚙️ Sistema y Configuración"
]
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos)

# =====================================================================
# 4. LÓGICA DE NAVEGACIÓN
# =====================================================================
if modulo_seleccionado == "🗂️ Gestión / Inventario":
    mostrar_formulario_inventario()

elif modulo_seleccionado == "📊 Panel Principal / Dashboard":
    st.markdown(f'<p class="welcome-title">Dashboard | {st.session_state.empresa}</p>', unsafe_allow_html=True)
    # ... resto de tu código de dashboard ...
else:
    st.title(modulo_seleccionado)
