import streamlit as st
import pandas as pd
import urllib.request
import json
from modulo_inventario import render_modulo_inventario

# =====================================================================
# 1. CONFIGURACIÓN Y ESTILOS (Mantenemos tu diseño)
# =====================================================================
st.set_page_config(page_title="GC Grupo Comercial C.A. - ERP", page_icon="💼", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #002366; } 
    .card-white { background-color: #003399; padding: 20px; border-radius: 14px; border: 1px solid #B87333; }
    h1, h2, h3, p, div { color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 2. LÓGICA DE TASAS (Mantenemos tu función BCV)
# =====================================================================
@st.cache_data(ttl=3600)
def obtener_tasas_bcv_reales():
    try:
        url = "https://ve.dispotech.workers.dev/"
        with urllib.request.urlopen(url, timeout=10) as response:
            datos = json.loads(response.read().decode())
        return float(datos['bcv']['usd']), float(datos['bcv']['eur'])
    except:
        return 42.35, 45.20

if 'tasa_bcb_usd' not in st.session_state:
    st.session_state.tasa_bcb_usd, st.session_state.tasa_bcb_eur = obtener_tasas_bcv_reales()
    st.session_state.tasa_binance = 46.50

st.session_state.referencia_master = st.session_state.tasa_binance

# =====================================================================
# 3. MENÚ DE NAVEGACIÓN (Corregido y consolidado)
# =====================================================================
st.sidebar.markdown("## ⚜️ GC - Grupo Comercial C.A.")
modulos = [
    "📊 Panel Principal / Dashboard", "🗂️ Gestión / Inventario", "🧾 Crear Factura (POS)", 
    "🛒 Compras a Proveedores", "📈 Reportes Generales"
]
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos)

# =====================================================================
# 4. DISTRIBUCIÓN DE MÓDULOS
# =====================================================================
if modulo_seleccionado == "📊 Panel Principal / Dashboard":
    st.title("Bienvenido al Dashboard")
    # Aquí puedes pegar el código de los KPIs que ya tenías
    
elif modulo_seleccionado == "🗂️ Gestión / Inventario":
    render_modulo_inventario() # Llama al módulo externo sin errores

else:
    st.title(modulo_seleccionado)
    st.info("Módulo en desarrollo.")
