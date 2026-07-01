import streamlit as st
import pandas as pd

# IMPORTACIONES (Deben ir al inicio para que el sistema reconozca los módulos)
from database_manager import init_db
from modulo_inventario import render_modulo_inventario
from modulo_pos import render_modulo_pos
from modulo_contable import render_modulo_contable
from dashboard import render_dashboard

# 1. CONFIGURACIÓN
st.set_page_config(page_title="GC Grupo Comercial C.A. - ERP", page_icon="💼", layout="wide")

# Inicialización de la base de datos central
init_db()

# 2. GESTIÓN DE TASAS PERSISTENTES
if 'tasa_binance' not in st.session_state: st.session_state.tasa_binance = 0.00
if 'tasa_bcv' not in st.session_state: st.session_state.tasa_bcv = 0.00

st.sidebar.markdown("## ⚜️ GC - Grupo Comercial C.A.")
st.sidebar.markdown("---")
st.session_state.tasa_binance = st.sidebar.number_input("Tasa Binance (P2P)", value=st.session_state.tasa_binance, format="%.2f")
st.session_state.tasa_bcv = st.sidebar.number_input("Tasa BCV", value=st.session_state.tasa_bcv, format="%.2f")

# 3. MENÚ DE NAVEGACIÓN
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", 
    ["📊 Dashboard", "🗂️ Gestión / Inventario", "🧾 POS", "🛒 Compras", "📈 Reportes"])

# 4. DISTRIBUCIÓN DE MÓDULOS (Llamado a funciones)
if modulo_seleccionado == "📊 Dashboard":
    render_dashboard()
elif modulo_seleccionado == "🗂️ Gestión / Inventario":
    render_modulo_inventario()
elif modulo_seleccionado == "🧾 POS":
    render_modulo_pos()
elif modulo_seleccionado == "🛒 Compras":
    render_modulo_contable()
elif modulo_seleccionado == "📈 Reportes":
    st.subheader("📈 Módulo de Reportes")
    st.info("Conectando con base de datos...")
