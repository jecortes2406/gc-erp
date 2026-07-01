Interfaz del sistema
import streamlit as st
import pandas as pd
import urllib.request
import json

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="GC Grupo Comercial C.A. - ERP",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. SISTEMA DE ESTILOS CSS INYECTADOS
# =====================================================================
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    
    /* Contenedores de Tarjetas */
    .card-white {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        border: 1px solid #E2E8F0;
    }
    .card-dark {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        padding: 25px;
        border-radius: 14px;
        margin-bottom: 15px;
    }
    
    /* Fuentes */
    .card-title { font-size: 13px; font-weight: 700; color: #64748B; text-transform: uppercase; }
    .card-title-dark { font-size: 13px; font-weight: 700; color: #38BDF8; text-transform: uppercase; }
    .card-value { font-size: 28px; font-weight: 700; color: #1E293B; }
    .card-value-dark { font-size: 36px; font-weight: 700; color: #FFFFFF; }
    .welcome-title { font-size: 28px; font-weight: 700; color: #0F172A; }
    .welcome-subtitle { font-size: 14px; color: #64748B; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. AUTOMATIZACIÓN: FUNCIÓN CONEXIÓN BCV EN VIVO (LIBRERÍA NATIVA)
# =====================================================================
@st.cache_data(ttl=3600)
def obtener_tasas_bcv_reales():
    """Consulta internet usando herramientas nativas para traer las tasas oficiales de Venezuela"""
    try:
        url = "https://ve.dispotech.workers.dev/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            datos = json.loads(response.read().decode())
        
        usd = float(datos['bcv']['usd'])
        eur = float(datos['bcv']['eur'])
        return usd, eur
    except Exception:
        # Valores de respaldo si internet o la API externa fallan
        return 42.35, 45.20

# Carga automática inicial
tasa_usd_bcv, tasa_eur_bcv = obtener_tasas_bcv_reales()

# Sincronización con el estado de la sesión
if 'tasa_bcb_usd' not in st.session_state:
    st.session_state.tasa_bcb_usd = tasa_usd_bcv
if 'tasa_bcb_eur' not in st.session_state:
    st.session_state.tasa_bcb_eur = tasa_eur_bcv
if 'tasa_binance' not in st.session_state:
    st.session_state.tasa_binance = 46.50

st.session_state.referencia_master = st.session_state.tasa_binance

# =====================================================================
# 4. PANEL IZQUIERDO: CONTROL CAMBIARIO EN COMPONENTES NATIVOS
# =====================================================================
st.sidebar.markdown("## ⚜️ GC")
st.sidebar.markdown("### Grupo Comercial C.A.")
st.sidebar.caption("Sistema Administrativo Integral v1.0")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🔄 CONTROL CAMBIARIO")

# Botón nativo de actualización forzada
if st.sidebar.button("🔄 Actualizar Tasas BCV", use_container_width=True):
    st.cache_data.clear()
    tasa_usd_bcv, tasa_eur_bcv = obtener_tasas_bcv_reales()
    st.session_state.tasa_bcb_usd = tasa_usd_bcv
    st.session_state.tasa_bcb_eur = tasa_eur_bcv
    st.rerun()

st.sidebar.markdown(" ")

# Lista vertical usando bloques nativos de alta estabilidad
st.sidebar.info(f"*💵 BCV USD:* \nBs. {st.session_state.tasa_bcb_usd:.2f}")
st.sidebar.info(f"*💶 BCV EUR:* \nBs. {st.session_state.tasa_bcb_eur:.2f}")

# Entrada manual de Binance
nueva_tasa = st
