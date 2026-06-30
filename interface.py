import streamlit as st
import pandas as pd
import datetime

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera instrucción)
# =====================================================================
st.set_page_config(
    page_title="GC Grupo Comercial C.A. - ERP",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. SISTEMA DE ESTILOS CSS INYECTADOS (Réplica de la Interfaz Base)
# =====================================================================
st.markdown("""
    <style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Contenedor de Tarjeta Blanca Estándar */
    .card-white {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 15px;
        border: 1px solid #E2E8F0;
    }
    
    /* Contenedor de Tarjeta Oscura (Utilidad Bruta) */
    .card-dark {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        padding: 25px;
        border-radius: 14px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    /* Títulos y Subtítulos dentro de Tarjetas */
    .card-title {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    .card-title-dark {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        color: #38BDF8;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    .card-value {
        font-size: 28px;
        font-weight: 700;
        color: #1E293B;
    }
    .card-value-dark {
        font-size: 36px;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    /* Estilos del Banner de Bienvenida */
    .welcome-title {
        font-size: 28px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 2px;
    }
    .welcome-subtitle {
        font-size: 14px;
        color: #64748B;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 3. INITIALIZATION DE ESTADOS GLOBALES (Cerebro de Datos)
# =====================================================================
if 'tasa_bcb_usd' not in st.session_state:
    st.session_state.tasa_bcb_usd = 42.35  # Simulación de carga automática inicial (BCB)
if 'tasa_bcb_eur' not in st.session_state:
    st.session_state.tasa_bcb_eur = 45.20  # Simulación de carga automática inicial (BCB)
if 'tasa_binance' not in st.session_state:
    st.session_state.tasa_binance = 46.50  # Control manual del administrador

# Cálculo de la Referencia Máster para la lógica interna de la empresa
st.session_state.referencia_master = st.session_state.tasa_binance

# =====================================================================
# 4. PANEL IZQUIERDO: SIMULACIÓN DE NAVEGACIÓN Y TASAS (Sidebar)
# =====================================================================
# Cabecera con identidad corporativa
st.sidebar.markdown("### 🏢 GC Grupo Comercial C.A.")
st.sidebar.caption("Sistema Administrativo Integral")
st.sidebar.markdown("---")

# Sub-panel de Control Cambiario (VE Reference)
st.sidebar.markdown("### 🔄 CONTROL CAMBIARIO")

col_tasa1, col_tasa2 = st.sidebar.columns(2)
with col_tasa1:
    st.metric(label="BCB USD (LIVE)", value=f"Bs. {st.session_state.tasa_bcb_usd:.2f}")
with col_tasa2:
    st.metric(label="BCB EUR (LIVE)", value=f"Bs. {st.session_state.tasa_bcb_eur:.2f}")

# Input Manual de Tasa Binance (Oculto para cálculos internos)
nueva_tasa_binance = st.sidebar.number_input(
    "Tasa Binance P2P (Manual):", 
    min_value=0.0, 
    value=st.session_state.tasa_binance,
    step=0.1
)
if nueva_tasa_binance != st.session_state.tasa_binance:
    st.session_state.tasa_binance = nueva_tasa_binance
    st.rerun()

st.sidebar.info(f"*REFERENCIA MASTER:* Bs. {st.session_state.referencia_master:.2f}")
st.sidebar.markdown("---")

# Menú de Navegación completo (Módulos que recibirán vida progresivamente)
modulos_sistema = [
    "📊 Panel Principal / Dashboard",
    "📦 Órdenes Online",
    "🧾 Crear Factura (POS)",
    "📑 Facturas Emitidas",
    "📝 Cotizaciones",
    "💰 Control de Cajas",
    "📉 Flujo de Caja",
    "👥 Cuentas x Cobrar",
    "⚠️ Notas de Crédito/Débito",
    "🛒 Compras a Proveedores",
    "🗂️ Gestión / Inventario",
    "📈 Reportes Generales",
    "⚙️ Sistema y Configuración"
]

modulo_activo = st.sidebar.radio("MENÚ DE OPERACIONES:", modulos_sistema)

# Footer estático del operador actual en el Sidebar
st.sidebar.markdown("---")
st.sidebar.caption("👤 *Usuario:* jecortes (ADMIN)")
st.sidebar.caption("📧 jecortes2406@gmail.com")

# =====================================================================
# 5. PANEL CENTRAL Y DERECHO (Layout del Dashboard Principal)
# =====================================================================
if modulo_activo == "📊 Panel Principal / Dashboard":
    
    # Estructuración de columnas principales: Centro (Contenido) y Derecha (Operaciones)
    col_panel_central, col_panel_derecho = st.columns([3.2, 0.8])
    
    with col_panel_central:
        # Bloque Superior: Mensaje de bienvenida
        st.markdown('<p class="welcome-title">¡Buenos días, jecortes!</p>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-subtitle">Aquí tienes el resumen operativo y financiero al momento.</p>', unsafe_allow_html=True)
        
        # Botones Rápidos Superiores en el Panel Central
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("➕ NUEVA VENTA", use_container_width=True):
                st.toast("Abriendo módulo de facturación rápida...")
        with col_btn2:
            if st.button("📄 COTIZAR", use_container_width=True):
                st.toast("Generando nueva plantilla de cotización...")
        with col_btn3:
            if st.button("📊 REPORTES", use_container_width=True):
                st.toast("Cargando analíticas financieras...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Sección de Métricas Destacadas (Fila 1)
        col_kpi_grande, col_kpi_caja, col_kpi_ingresos = st.columns([1.6, 1.2, 1.2])
        
        with col_kpi_grande:
            st.markdown(f"""
                <div class="card-dark">
                    <div class="card-title-dark">Utilidad Bruta (Mes)</div>
                    <div class="card-value-dark">$1,447.00</div>
                    <small style="color: #4ADE80;">📈 +12% respecto al mes anterior</small>
                </div>
                """, unsafe_allow_html=True)
                
        with col_kpi_caja:
            st.markdown("""
                <div class="card-white">
                    <div class="card-title">Caja Real (En Mano)</div>
                    <div class="card-value">$10.00</div>
                    <small style="color: #64748B;">Efectivo disponible</small>
                </div>
                """, unsafe_allow_html=True)
                
        with col_kpi_ingresos:
            st.markdown("""
                <div class="card-white">
                    <div class="card-title">Ingresos Hoy</div>
                    <div class="card-value">$0.00</div>
                    <small style="color: #64748B;">Ayer: $0.00</small>
                </div>
                """, unsafe_allow_html=True)

        # Sección de Métricas Destacadas (Fila 2)
        col_kpi_cobrar, col_kpi_pagar, col_kpi_ticket, col_kpi_stock = st.columns(4)
        with col_kpi_cobrar:
            st.markdown("""
                <div class="card-white"><div class="card-title">Por Cobrar</div><div class="card-value">$0.00</div><small>Créditos activos</small></div>
                """, unsafe_allow_html=True)
        with col_kpi_pagar:
            st.markdown("""
                <div class="card-white"><div class="card-title">Por Pagar</div><div class="card-value">$0.00</div><small>Pasivos comerciales</small></div>
                """, unsafe_allow_html=True)
        with col_kpi_ticket:
            st.markdown("""
                <div class="card-white"><div class="card-title">Ticket Medio</div><div class="card-value">$0.00</div><small>Promedio diario</small></div>
                """, unsafe_allow_html=True)
        with col_kpi_stock:
            st.markdown("""
                <div class="card-white"><div class="card-title" style="color: #EF4444;">Stock Crítico</div><div class="card-value">0</div><small>Alertas de inventario</small></div>
                """, unsafe_allow_html=True)

        # Fila de Monitoreo Intermedio
        st.markdown("""
            <div class="card-white">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="card-title" style="font-size:14px;">📉 Movimientos de Caja</span>
                    <span style="font-size: 12px; color:#1E3A8A; font-weight:bold; cursor:pointer;">VER FLUJO</span>
                </div>
                <p style="text-align: center; color: #94A3B8; padding: 20px 0;">SIN MOVIMIENTOS REGISTRADOS EN EL TURNO</p>
            </div>
            """, unsafe_allow_html=True)

        # Fila de Reportes Inferiores (Top Ventas)
        col_top1, col_top2 = st.columns(2)
        with col_top1:
            st.markdown("""
                <div class="card-white">
                    <div class="card-title">🔵 Top Tienda Física</div>
                    <p style="text-align: center; color: #94A3B8; padding: 10px 0;">SIN DATOS DISPONIBLES</p>
                </div>
                """, unsafe_allow_html=True)
        with col_top2:
            st.markdown("""
                <div class="card-white">
                    <div class="card-title">🌐 Top E-Commerce</div>
                    <p style="text-align: center; color: #94A3B8; padding: 10px 0;">SIN DATOS DISPONIBLES</p>
                </div>
                """, unsafe_allow_html=True)
                
        # Última fila del Panel Central
        col_inf1, col_inf2 = st.columns([2.5, 1.5])
        with col_inf1:
            st.markdown("""
                <div class="card-white">
                    <div class="card-title">🛒 Últimas Ventas</div>
                    <p style="text-align: center; color: #94A3B8; padding: 10px 0;">SIN VENTAS RECIENTES</p>
                </div>
                """, unsafe_allow_html=True)
        with col_inf2:
            st.markdown("""
                <div class="card-white">
                    <div class="card-title" style="color: #EF4444;">⚠️ Stock Crítico</div>
                    <p style="text-align: center; color: #4ADE80; font-weight: bold; padding: 10px 0;">TODO EN ORDEN</p>
                </div>
                """, unsafe_allow_html=True)

    with col_panel_derecho:
        # Espacio dedicado a la Pasarela Operativa Dinámica (Bloque Derecho de Facturación)
        st.markdown("""
            <div class="card-white" style="background-color: #EFF6FF; border: 1px solid #BFDBFE; height: 100%;">
                <div class="card-title" style="color: #1E40AF;">🛒 MÓDULO OPERATIVO</div>
                <p style="font-size:12px; color: #1E3A8A;">Este panel se activa al facturar, cotizar o realizar comparativas.</p>
                <hr style="border-color: #BFDBFE;">
            </div>
            """, unsafe_allow_html=True)
            
        # Contenedor dinámico interactivo para pruebas de la Capa 1
        st.info("⚡ Bloque de Acción en Vivo")
        st.caption("Los artículos seleccionados en el panel central se totalizarán de forma automática en este bloque.")

# =====================================================================
# LÓGICA DE CONMUTACIÓN DE MÓDULOS (Espacios reservados para las fases de automatización)
# =====================================================================
else:
    st.title(modulo_activo)
    st.info(f"El contenedor para el módulo de '{modulo_activo}' está listo en la arquitectura de la Capa 1.")
    st.markdown("---")
    st.write("Presiona 'Panel Principal / Dashboard' en el menú izquierdo para regresar a la vista maestra.")
