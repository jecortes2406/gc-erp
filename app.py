import streamlit as st
import pandas as pd
import urllib.request
import json
import datetime

# Importaciones de módulos del sistema
from database_manager import init_db
from modulo_inventario import mostrar_formulario_inventario

# =====================================================================
# 1. CONFIGURACIÓN INICIAL Y ESTADOS
# =====================================================================
st.set_page_config(
    page_title="GC Grupo Comercial C.A. - ERP",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar Base de Datos de forma segura
try:
    init_db()
except Exception as e:
    st.error(f"❌ Error al inicializar la base de datos: {e}")

# =====================================================================
# 2. FUNCIONES DE MONITOREO Y APIS (OPTIMIZADAS CON CACHÉ)
# =====================================================================
@st.cache_data(ttl=3600)  # Guarda en caché por 1 hora para evitar peticiones infinitas
def obtener_tasas_cambio():
    """
    Simulación o consulta real de tasas de cambio con fallback seguro.
    Modifica las URLs por tus endpoints reales de BCB o Binance.
    """
    tasas = {
        "bcb_usd": 42.35,
        "binance_usdt": 46.50
    }
    # Ejemplo de estructura de consumo real (descomentar al conectar la API):
    # try:
    #     req = urllib.request.Request("TU_API_URL", headers={'User-Agent': 'Mozilla/5.0'})
    #     with urllib.request.urlopen(req) as response:
    #         data = json.loads(response.read().decode())
    #         tasas["bcb_usd"] = float(data.get("usd", 42.35))
    # except Exception:
    #     pass # Si falla, mantiene los valores por defecto (fallback)
    return tasas

# Carga de variables en el Estado de la Sesión (Session State)
if 'empresa' not in st.session_state: 
    st.session_state.empresa = "Grupo Comercial C.A."

# Sincronizar tasas dinámicas
tasas_actuales = obtener_tasas_cambio()
st.session_state.tasa_bcb_usd = tasas_actuales["bcb_usd"]
st.session_state.tasa_binance = tasas_actuales["binance_usdt"]

# =====================================================================
# 3. INTERFAZ: SIDEBAR (MENÚ NAV)
# =====================================================================
with st.sidebar:
    st.markdown(f"## ⚜️ {st.session_state.empresa}")
    st.markdown("---")
    
    modulo_seleccionado = st.radio(
        "MENÚ DE OPERACIONES:", 
        [
            "📊 Panel Principal / Dashboard",
            "🗂️ Gestión / Inventario",
            "🧾 Crear Factura (POS)"
        ],
        index=0
    )
    
    st.markdown("---")
    # Indicador de Tasas en tiempo real en la barra lateral
    st.markdown("### 💸 Tasas de Cambio")
    st.caption(f"📅 Actualizado: {datetime.date.today().strftime('%d/%m/%Y')}")
    st.metric(label="BCB (USD)", value=f"{st.session_state.tasa_bcb_usd:.2f} Bs.")
    st.metric(label="Binance (USDT)", value=f"{st.session_state.tasa_binance:.2f} Bs.")

# =====================================================================
# 4. COMPONENTES VISUALES (MÓDULOS DE VISTA)
# =====================================================================
def renderizar_dashboard():
    """Renderiza la vista del cuadro de mando financiero."""
    col_centro, col_derecha = st.columns([3.2, 0.8])
    
    with col_centro:
        st.title(f"Dashboard | {st.session_state.empresa}")
        st.subheader("Resumen operativo y financiero al momento")
        
        # Botones de Acción Rápida (Layout moderno)
        cb1, cb2, cb3 = st.columns(3)
        if cb1.button("➕ NUEVA VENTA", use_container_width=True, type="primary"):
            st.toast("Abriendo módulo de ventas...") # Reemplazar con lógica real de redirección
        if cb2.button("📄 COTIZAR", use_container_width=True):
            st.toast("Generando nueva cotización...")
        if cb3.button("📊 REPORTES EXPORTABLES", use_container_width=True):
            st.toast("Preparando descarga de reportes...")
            
        st.write("---")
        
        # Fila Principal de KPIs Financieros (Uso de st.columns nativo)
        k_g, k_c, k_i = st.columns(3)
        with k_g:
            with st.container(border=True):
                st.metric(label="💵 Utilidad Bruta (Mes)", value="$1,447.00", delta="+12% vs mes anterior")
        with k_c:
            with st.container(border=True):
                st.metric(label="🏦 Caja Real (En Mano)", value="$10.00", delta=None, help="Efectivo físico disponible en caja fuerte")
        with k_i:
            with st.container(border=True):
                st.metric(label="📈 Ingresos Hoy", value="$0.00", delta="$0.00 (Ayer)")

        # Segunda Fila de KPIs (Métricas de Control)
        st.write("")
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            with st.container(border=True): st.metric(label="Por Cobrar", value="$0.00")
        with k2:
            with st.container(border=True): st.metric(label="Por Pagar", value="$0.00")
        with k3:
            with st.container(border=True): st.metric(label="Ticket Medio", value="$0.00")
        with k4:
            with st.container(border=True): 
                # Alerta visual si hay stock crítico
                stock_critico = 0
                st.metric(
                    label="🚨 Stock Crítico", 
                    value=str(stock_critico), 
                    delta="-5 productos" if stock_critico > 0 else None,
                    delta_color="inverse"
                )
    
    with col_derecha:
        with st.container(border=True):
            st.markdown("### 🛒 MÓDULO OPERATIVO")
            st.markdown("---")
            st.info("Resumen rápido de las actividades operacionales asignadas para el día de hoy.")
            st.checkbox("Verificar cierres de caja pendientes", value=False)
            st.checkbox("Validar transferencias bancarias", value=True)

# =====================================================================
# 5. CONTROLADOR DE ENRUTAMIENTO PRINCIPAL
# =====================================================================
if modulo_seleccionado == "📊 Panel Principal / Dashboard":
    renderizar_dashboard()

elif modulo_seleccionado == "🗂️ Gestión / Inventario":
    st.title("🗂️ Control de Inventarios")
    mostrar_formulario_inventario()

elif modulo_seleccionado == "🧾 Crear Factura (POS)":
    st.title("🧾 Módulo de Facturación Electrónica (POS)")
    st.info("🛠️ Funcionalidad de punto de venta (POS) actualmente en desarrollo e integración de hardware.")

else:
    st.warning("⚠️ Módulo no reconocido o fuera de servicio temporal.")
