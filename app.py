import streamlit as st

def run():
    st.markdown("## 🏢 GESTIÓN DE INVENTARIO")
    
    # Usamos la clase .card-white definida en tu app.py
    with st.container():
        st.markdown('<div class="card-white">', unsafe_allow_html=True)
        st.subheader("📝 NUEVO PRODUCTO")
        
        c1, c2 = st.columns(2)
        sku = c1.text_input("Código SKU")
        nombre = c2.text_input("Nombre del Producto")
        
        c3, c4, c5 = st.columns(3)
        costo = c3.number_input("Costo (USD)")
        precio_detal = c4.number_input("Precio Detal (USD)")
        precio_mayor = c5.number_input("Precio Mayor (USD)")
        
        if st.button("🚀 GUARDAR EN BASE DE DATOS", type="primary"):
            st.success("Producto registrado anclado a Binance.")
        st.markdown('</div>', unsafe_allow_html=True)
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
# 2. SISTEMA DE ESTILOS: AZUL REY Y BRONCE/COBRE
# =====================================================================
st.markdown("""
    <style>
    /* Fondo Azul Rey Oscuro */
    .stApp { background-color: #002366; } 
    
    /* Contenedores de Tarjetas (Fondo azul un poco más claro para contraste) */
    .card-white {
        background-color: #003399;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 15px;
        border: 1px solid #B87333; /* Borde Bronce */
    }
    
    .card-dark {
        background: linear-gradient(135deg, #001a4d 0%, #002366 100%);
        color: #CD7F32; /* Bronce */
        padding: 25px;
        border-radius: 14px;
        margin-bottom: 15px;
        border: 1px solid #B87333;
    }
    
    /* Fuentes en tonos Bronce/Cobre */
    .card-title { font-size: 13px; font-weight: 700; color: #CD7F32; text-transform: uppercase; }
    .card-title-dark { font-size: 13px; font-weight: 700; color: #E5A86D; text-transform: uppercase; }
    .card-value { font-size: 28px; font-weight: 700; color: #FFFFFF; }
    .card-value-dark { font-size: 36px; font-weight: 700; color: #FFFFFF; }
    .welcome-title { font-size: 28px; font-weight: 700; color: #CD7F32; }
    .welcome-subtitle { font-size: 14px; color: #FFFFFF; margin-bottom: 20px; }
    
    /* Ajuste para texto de Streamlit que no sea clase */
    h1, h2, h3, p, div { color: #FFFFFF; }
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

# 1. BOTÓN DE AUTOMATIZACIÓN (MANTENEMOS LA FUNCIÓN)
if st.sidebar.button("🔄 Actualizar Tasas BCV", use_container_width=True):
    st.cache_data.clear()
    tasa_usd_bcv, tasa_eur_bcv = obtener_tasas_bcv_reales()
    st.session_state.tasa_bcb_usd = tasa_usd_bcv
    st.session_state.tasa_bcb_eur = tasa_eur_bcv
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("📌 Edición Manual:")

# 2. EDICIÓN MANUAL (ANEXAMOS ESTA NUEVA FUNCIÓN)
st.session_state.tasa_bcb_usd = st.sidebar.number_input(
    "💵 BCV USD (Manual):", value=st.session_state.tasa_bcb_usd, format="%.2f"
)
st.session_state.tasa_bcb_eur = st.sidebar.number_input(
    "💶 BCV EUR (Manual):", value=st.session_state.tasa_bcb_eur, format="%.2f"
)

st.session_state.tasa_binance = st.sidebar.number_input(
    "💎 Tasa Binance P2P (Manual):", 
    value=st.session_state.tasa_binance, 
    step=0.1,
    format="%.2f"
)

st.session_state.referencia_master = st.session_state.tasa_binance
st.sidebar.warning(f"*REFERENCIA MASTER:* \nBs. {st.session_state.referencia_master:.2f}")
st.sidebar.markdown("---")
# Menú de Operaciones
modulos = [
    "📊 Panel Principal / Dashboard", "📦 Órdenes Online", "🧾 Crear Factura (POS)", 
    "📑 Facturas Emitidas", "📝 Cotizaciones", "💰 Control de Cajas", 
    "📉 Flujo de Caja", "👥 Cuentas x Cobrar", "⚠️ Notas de Crédito/Débito", 
    "🛒 Compras a Proveedores", "🗂️ Gestión / Inventario", "📈 Reportes Generales", 
    "⚙️ Sistema y Configuración"
]
modulo_seleccionado = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos)

st.sidebar.markdown("---")
st.sidebar.caption("👤 *Usuario:* jecortes (ADMIN)\n\n📧 jecortes2406@gmail.com")

# =====================================================================
# 5. PANEL CENTRAL Y DERECHO (Layout de Trabajo Principal)
# =====================================================================
if modulo_seleccionado == "📊 Panel Principal / Dashboard":
    col_centro, col_derecha = st.columns([3.2, 0.8])
    
    with col_centro:
        st.markdown('<p class="welcome-title">¡Buenos días, jecortes!</p>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-subtitle">Aquí tienes el resumen operativo y financiero al momento.</p>', unsafe_allow_html=True)
        
        # Botones Rápidos
        cb1, cb2, cb3 = st.columns(3)
        cb1.button("➕ NUEVA VENTA", use_container_width=True)
        cb2.button("📄 COTIZAR", use_container_width=True)
        cb3.button("📊 REPORTES", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # KPIs Fila 1
        k_g, k_c, k_i = st.columns([1.6, 1.2, 1.2])
        with k_g:
            st.markdown(f'<div class="card-dark"><div class="card-title-dark">Utilidad Bruta (Mes)</div><div class="card-value-dark">$1,447.00</div><small style="color: #4ADE80;">📈 +12%</small></div>', unsafe_allow_html=True)
        with k_c:
            st.markdown('<div class="card-white"><div class="card-title">Caja Real (En Mano)</div><div class="card-value">$10.00</div><small>Efectivo disponible</small></div>', unsafe_allow_html=True)
        with k_i:
            st.markdown('<div class="card-white"><div class="card-title">Ingresos Hoy</div><div class="card-value">$0.00</div><small>Ayer: $0.00</small></div>', unsafe_allow_html=True)

        # KPIs Fila 2
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown('<div class="card-white"><div class="card-title">Por Cobrar</div><div class="card-value">$0.00</div></div>', unsafe_allow_html=True)
        k2.markdown('<div class="card-white"><div class="card-title">Por Pagar</div><div class="card-value">$0.00</div></div>', unsafe_allow_html=True)
        k3.markdown('<div class="card-white"><div class="card-title">Ticket Medio</div><div class="card-value">$0.00</div></div>', unsafe_allow_html=True)
        k4.markdown('<div class="card-white"><div class="card-title" style="color:#EF4444;">Stock Crítico</div><div class="card-value">0</div></div>', unsafe_allow_html=True)

        # Monitoreo Inferior
        st.markdown('<div class="card-white"><div class="card-title">📉 Movimientos de Caja</div><p style="text-align: center; color: #94A3B8; padding: 15px 0;">SIN MOVIMIENTOS REGISTRADOS</p></div>', unsafe_allow_html=True)
        
        c_t1, c_t2 = st.columns(2)
        c_t1.markdown('<div class="card-white"><div class="card-title">🔵 Top Tienda Física</div><p style="text-align: center; color: #94A3B8;">SIN DATOS</p></div>', unsafe_allow_html=True)
        c_t2.markdown('<div class="card-white"><div class="card-title">🌐 Top E-Commerce</div><p style="text-align: center; color: #94A3B8;">SIN DATOS</p></div>', unsafe_allow_html=True)

        f1, f2 = st.columns([2.5, 1.5])
        f1.markdown('<div class="card-white"><div class="card-title">🛒 Últimas Ventas</div><p style="text-align: center; color: #94A3B8;">SIN VENTAS RECIENTES</p></div>', unsafe_allow_html=True)
        f2.markdown('<div class="card-white"><div class="card-title" style="color: #EF4444;">⚠️ Stock Crítico</div><p style="text-align: center; color: #4ADE80; font-weight: bold;">TODO EN ORDEN</p></div>', unsafe_allow_html=True)

    with col_derecha:
        st.markdown('<div class="card-white" style="background-color: #EFF6FF; border: 1px solid #BFDBFE; height: 100%;"><div class="card-title" style="color: #1E40AF;">🛒 MÓDULO OPERATIVO</div><br><p style="font-size:12px; color: #1E3A8A;">Este panel se activará dinámicamente al facturar o cotizar artículos en las fases superiores.</p></div>', unsafe_allow_html=True)

else:
    st.title(modulo_seleccionado)
    st.info("Estructura de la Capa 1 lista para recibir la automatización de este módulo.")
