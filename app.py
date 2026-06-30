import streamlit as st
import pandas as pd
import urllib.request
import json


from database_manager import init_db
from modulo_inventario import mostrar_formulario_inventario
# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTADOS GLOBALES
# =====================================================================
st.set_page_config(
    page_title="GC Grupo Comercial C.A. - ERP",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)
init_db()
# Inicialización de variables de estado para persistencia
if 'empresa' not in st.session_state:
    st.session_state.empresa = "Grupo Comercial C.A."
if 'tasa_binance' not in st.session_state:
    st.session_state.tasa_binance = 46.50
if 'tasa_bcb_usd' not in st.session_state:
    st.session_state.tasa_bcb_usd = 42.35
if 'tasa_bcb_eur' not in st.session_state:
    st.session_state.tasa_bcb_eur = 45.20

# =====================================================================
# 2. SISTEMA DE ESTILOS CSS INYECTADOS
# =====================================================================
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .card-white { background-color: #FFFFFF; padding: 20px; border-radius: 14px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 15px; border: 1px solid #E2E8F0; }
    .card-dark { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #FFFFFF; padding: 25px; border-radius: 14px; margin-bottom: 15px; }
    .card-title { font-size: 13px; font-weight: 700; color: #64748B; text-transform: uppercase; }
    .card-title-dark { font-size: 13px; font-weight: 700; color: #38BDF8; text-transform: uppercase; }
    .card-value { font-size: 28px; font-weight: 700; color: #1E293B; }
    .card-value-dark { font-size: 36px; font-weight: 700; color: #FFFFFF; }
    .welcome-title { font-size: 28px; font-weight: 700; color: #0F172A; }
    .welcome-subtitle { font-size: 14px; color: #64748B; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. AUTOMATIZACIÓN: FUNCIÓN CONEXIÓN BCV
# =====================================================================
@st.cache_data(ttl=3600)
def obtener_tasas_bcv_reales():
    try:
        url = "https://ve.dispotech.workers.dev/"
        # Añadimos un User-Agent explícito para evitar bloqueos
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            datos = json.loads(response.read().decode())
        return float(datos['bcv']['usd']), float(datos['bcv']['eur'])
    except Exception:
        return st.session_state.tasa_bcb_usd, st.session_state.tasa_bcb_eur

# =====================================================================
# 4. PANEL IZQUIERDO: CONFIGURACIÓN Y CONTROL
# =====================================================================
st.sidebar.markdown("## ⚜️ GC")
st.sidebar.markdown(f"### {st.session_state.empresa}")
st.sidebar.caption("Sistema Administrativo Integral 1.0")
st.sidebar.markdown("---")

st.sidebar.markdown("### ⚙️ CONFIGURACIÓN")
st.session_state.empresa = st.sidebar.text_input("Nombre de la Empresa:", st.session_state.empresa)

st.sidebar.markdown("### 🔄 CONTROL CAMBIARIO")

if st.sidebar.button("🔄 Actualizar Tasas BCV", use_container_width=True):
    tasa_usd, tasa_eur = obtener_tasas_bcv_reales()
    st.session_state.tasa_bcb_usd = tasa_usd
    st.session_state.tasa_bcb_eur = tasa_eur
    st.rerun()

st.sidebar.info(f"💵 BCV USD: Bs. {st.session_state.tasa_bcb_usd:.2f}")
st.sidebar.info(f"💶 BCV EUR: Bs. {st.session_state.tasa_bcb_eur:.2f}")

st.session_state.tasa_binance = st.sidebar.number_input(
    "Tasa Binance P2P (Manual):", min_value=0.0, value=st.session_state.tasa_binance, step=0.1
)
st.sidebar.warning(f"REFERENCIA MASTER: Bs. {st.session_state.tasa_binance:.2f}")
st.sidebar.markdown("---")

modulos = [
    "📊 Panel Principal / Dashboard", "📦 Órdenes Online", "🧾 Crear Factura (POS)", 
    "📑 Facturas Emitidas", "📝 Cotizaciones", "💰 Control de Cajas", 
    "📉 Flujo de Caja", "👥 Cuentas x Cobrar", "⚠️ Notas de Crédito/Débito", 
    "🛒 Compras a Proveedores", "🗂️ Gestión / Inventario", "📈 Reportes Generales", 
    "Gestion / Inventario"
    "⚙️ Sistema y Configuración"
]
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos)

# --- CONEXIÓN DEL MÓDULO ---
if "Gestión / Inventario" in modulo_seleccionado:
    mostrar_formulario_inventario()
# =====================================================================
# 5. PANEL CENTRAL
# =====================================================================
if modulo_seleccionado == "📊 Panel Principal / Dashboard":
    col_centro, col_derecha = st.columns([3.2, 0.8])
    with col_centro:
        st.markdown(f'<p class="welcome-title">Dashboard | {st.session_state.empresa}</p>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-subtitle">Aquí tienes el resumen operativo y financiero al momento.</p>', unsafe_allow_html=True)
        
        # [Código de KPIs y Tarjetas permanece exactamente igual]
        cb1, cb2, cb3 = st.columns(3)
        cb1.button("➕ NUEVA VENTA", use_container_width=True)
        cb2.button("📄 COTIZAR", use_container_width=True)
        cb3.button("📊 REPORTES", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        k_g, k_c, k_i = st.columns([1.6, 1.2, 1.2])
        with k_g:
            st.markdown(f'<div class="card-dark"><div class="card-title-dark">Utilidad Bruta (Mes)</div><div class="card-value-dark">$1,447.00</div><small style="color: #4ADE80;">📈 +12%</small></div>', unsafe_allow_html=True)
        with k_c:
            st.markdown('<div class="card-white"><div class="card-title">Caja Real (En Mano)</div><div class="card-value">$10.00</div><small>Efectivo disponible</small></div>', unsafe_allow_html=True)
        with k_i:
            st.markdown('<div class="card-white"><div class="card-title">Ingresos Hoy</div><div class="card-value">$0.00</div><small>Ayer: $0.00</small></div>', unsafe_allow_html=True)

        k1, k2, k3, k4 = st.columns(4)
        k1.markdown('<div class="card-white"><div class="card-title">Por Cobrar</div><div class="card-value">$0.00</div></div>', unsafe_allow_html=True)
        k2.markdown('<div class="card-white"><div class="card-title">Por Pagar</div><div class="card-value">$0.00</div></div>', unsafe_allow_html=True)
        k3.markdown('<div class="card-white"><div class="card-title">Ticket Medio</div><div class="card-value">$0.00</div></div>', unsafe_allow_html=True)
        k4.markdown('<div class="card-white"><div class="card-title" style="color:#EF4444;">Stock Crítico</div><div class="card-value">0</div></div>', unsafe_allow_html=True)
    
    with col_derecha:
        st.markdown('<div class="card-white" style="background-color: #EFF6FF; border: 1px solid #BFDBFE; height: 100%;"><div class="card-title" style="color: #1E40AF;">🛒 MÓDULO OPERATIVO</div><br><p style="font-size:12px; color: #1E3A8A;">Panel dinámico activo.</p></div>', unsafe_allow_html=True)
else:
    st.title(modulo_seleccionado)
