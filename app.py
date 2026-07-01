import streamlit as st
from database_manager import init_db
import pandas as pd
import urllib.request
import json

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA (SIEMPRE PRIMERO)
# =====================================================================
st.set_page_config(
    page_title="GC Grupo Comercial C.A. - ERP",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializamos la base de datos al arrancar
init_db()

# =====================================================================
# 2. SISTEMA DE ESTILOS
# =====================================================================
st.markdown("""
    <style>
    .stApp { background-color: #002366; } 
    .card-white {
        background-color: #003399;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 15px;
        border: 1px solid #B87333;
    }
    .card-dark {
        background: linear-gradient(135deg, #001a4d 0%, #002366 100%);
        color: #CD7F32;
        padding: 25px;
        border-radius: 14px;
        margin-bottom: 15px;
        border: 1px solid #B87333;
    }
    .card-title { font-size: 13px; font-weight: 700; color: #CD7F32; text-transform: uppercase; }
    .card-title-dark { font-size: 13px; font-weight: 700; color: #E5A86D; text-transform: uppercase; }
    .card-value { font-size: 28px; font-weight: 700; color: #FFFFFF; }
    .card-value-dark { font-size: 36px; font-weight: 700; color: #FFFFFF; }
    .welcome-title { font-size: 28px; font-weight: 700; color: #CD7F32; }
    .welcome-subtitle { font-size: 14px; color: #FFFFFF; margin-bottom: 20px; }
    h1, h2, h3, p, div { color: #FFFFFF; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. AUTOMATIZACIÓN: TASAS BCV
# =====================================================================
@st.cache_data(ttl=3600)
def obtener_tasas_bcv_reales():
    try:
        url = "https://ve.dispotech.workers.dev/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            datos = json.loads(response.read().decode())
        return float(datos['bcv']['usd']), float(datos['bcv']['eur'])
    except Exception:
        return 42.35, 45.20

tasa_usd_bcv, tasa_eur_bcv = obtener_tasas_bcv_reales()

if 'tasa_bcb_usd' not in st.session_state: st.session_state.tasa_bcb_usd = tasa_usd_bcv
if 'tasa_bcb_eur' not in st.session_state: st.session_state.tasa_bcb_eur = tasa_eur_bcv
if 'tasa_binance' not in st.session_state: st.session_state.tasa_binance = 46.50
st.session_state.referencia_master = st.session_state.tasa_binance

# =====================================================================
# 4. SIDEBAR Y MENÚ
# =====================================================================
st.sidebar.markdown("## ⚜️ GC")
st.sidebar.markdown("### Grupo Comercial C.A.")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 CONTROL CAMBIARIO")

if st.sidebar.button("🔄 Actualizar Tasas BCV", use_container_width=True):
    st.cache_data.clear()
    tasa_usd_bcv, tasa_eur_bcv = obtener_tasas_bcv_reales()
    st.session_state.tasa_bcb_usd = tasa_usd_bcv
    st.session_state.tasa_bcb_eur = tasa_eur_bcv
    st.rerun()

st.sidebar.session_state.tasa_bcb_usd = st.sidebar.number_input("💵 BCV USD:", value=st.session_state.tasa_bcb_usd, format="%.2f")
st.session_state.tasa_binance = st.sidebar.number_input("💎 Binance:", value=st.session_state.tasa_binance, format="%.2f")
st.session_state.referencia_master = st.session_state.tasa_binance
st.sidebar.warning(f"REFERENCIA MASTER: Bs. {st.session_state.referencia_master:.2f}")

modulos = ["📊 Panel Principal / Dashboard", "🧾 Crear Factura (POS)", "🗂️ Gestión / Inventario"]
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos)

# =====================================================================
# 5. LÓGICA DE NAVEGACIÓN
# =====================================================================
# --- LÓGICA DE NAVEGACIÓN ---
# Asegúrate de que este bloque esté al final de tu archivo app.py
if modulo_seleccionado == "🧾 Crear Factura (POS)":
    import modulo_pos
    modulo_pos.render_modulo_pos()

elif modulo_seleccionado == "🗂️ Gestión / Inventario":
    # Llamamos a la función que importaste al inicio
    render_modulo_inventario()

else:
    st.title("GC Grupo Comercial C.A.")
    st.info("Seleccione una opción en el menú lateral para comenzar.")
