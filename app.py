import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse

# =====================================================================
# MOTOR DE INICIALIZACIÓN Y AUTO-MIGRACIÓN DE BASE DE DATOS
# =====================================================================
def inicializar_estructura_erp():
    conn = sqlite3.connect('gc_ecosistema_data_v4.db')
    cursor = conn.cursor()
    
    # 1. Parámetros de Configuración y Tasas del Día
    cursor.execute('''CREATE TABLE IF NOT EXISTS configuracion (
                        id INTEGER PRIMARY KEY, nombre_empresa TEXT, color_marca TEXT,
                        tasa_bcv REAL, tasa_euro REAL, tasa_binance REAL, comision_vendedor_porc REAL)''')
    
    # 2. Maestro de Inventario con Costo y 3 Tipos de Precios Independientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
                        id INTEGER PRIMARY KEY, nombre TEXT, costo_usd REAL, porc_ganancia REAL,
                        precio_detal_ves REAL, precio_bulto_ves REAL, precio_mayor_ves REAL,
                        lote_zeta TEXT, stock INTEGER, dias_stock INTEGER, rotacion TEXT)''')
    
    # 3. Libro de Ventas con Desglose Fiscal Obligatorio (IVA, IGTF, Comisión)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, cliente_id TEXT, vendedor TEXT,
                        codigo_producto INTEGER, cantidad INTEGER, precio_aplicado_ves REAL, 
                        subtotal_ves REAL, iva_ves REAL, igtf_ves REAL, total_ves REAL,
                        equivalente_usd REAL, comision_ganada_usd REAL, forma_pago TEXT, moneda TEXT)''')
    
    # 4. Directorio de Contactos Comerciales
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (rif_cedula TEXT PRIMARY KEY, nombre TEXT, telefono TEXT, direccion TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (rif TEXT PRIMARY KEY, empresa TEXT, telefono TEXT, contacto TEXT)''')
    
    # 5. Libro de Egresos y Gastos Multimoneda
    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, descripcion TEXT,
                        monto_original REAL, moneda TEXT, tasa_cambio REAL, equivalente_usd REAL, proveedor_rif TEXT)''')
    
    # Inyectar muestras comerciales iniciales si el sistema está vacío
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO configuracion VALUES (1, 'Grupo Comercial, C.A.', '#1B4F72', 45.50633, 49.33210, 47.85350, 5.0)")
    
    cursor.execute("SELECT COUNT(*) FROM inventario")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO inventario VALUES (1061, 'BIANCHI CARAMELO CHOCOLATE 18BX100U', 30.00, 25.00, 1740.00, 1600.00, 1550.00, 'Z-101', 183, 0, 'Alta')")
        cursor.execute("INSERT INTO inventario VALUES (1092, 'TRULULU AROS 36BX50U (HUESO)', 50.00, 30.00, 3020.00, 2800.00, 2700.00, 'Z-Hueso', 38, 29, 'Hueso')")
        cursor.execute("INSERT INTO clientes VALUES ('J-123456780', 'Distribuidora Surtidora Central, C.A.', '584121234567', 'Caracas, Distrito Capital')")
        cursor.execute("INSERT INTO proveedores VALUES ('J-999999990', 'Confiterías El Bulto Mayorista', '584149876543', 'Maracay Almacenes')")
    
    conn.commit()
    conn.close()

inicializar_estructura_erp()

# Extraer parámetros globales de configuración de forma segura
conn = sqlite3.connect('gc_ecosistema_data_v4.db')
cfg = pd.read_sql_query("SELECT * FROM configuracion WHERE id=1", conn).iloc[0]
conn.close()

# Configuración del Entorno de Alta Visibilidad
st.set_page_config(page_title=f"{cfg['nombre_empresa']} - ERP Legal Venezuela", layout="wide", page_icon="🏢")

# Inyección de Estilos CSS Gerenciales (Fondo Claro, Alta Definición)
st.markdown(f"""
    <style>
        .main {{ background-color: #f8f9fa; color: #1e293b; }}
        .stApp {{ background-color: #f8f9fa; }}
        h1, h2, h3 {{ color: {cfg['color_marca']} !important; font-family: 'Segoe UI', sans-serif; font-weight: 600; }}
        div[data-testid="stMetric"] {{ background-color: #ffffff; padding: 18px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        div[data-testid="stMetricLabel"] {{ color: #64748b !important; font-weight: 500; font-size: 14px; }}
        div[data-testid="stMetricValue"] {{ color: #0f172a !important; font-weight: 700; font-size: 24px; }}
        .stButton>button {{ background-color: #e67e22; color: white; border-radius: 5px; border: none; font-weight: bold; width: 100%; height: 40px; }}
        .stButton>button:hover {{ background-color: #d35400; color: white; }}
        section[data-testid="stSidebar"] {{ background-color: #0f172a !important; }}
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] p {{ color: #ffffff !important; }}
        section[data-testid="stSidebar"] label {{ color: #94a3b8 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- MENÚ LATERAL IZQUIERDO (SIDEBAR CORPORATIVO) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom:0;'>GC</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-weight: bold; font-size:12px;'>{cfg['nombre_empresa'].upper()}<br><small style='color:#e67e22;'>ERP COMPLIANCE V4.0</small></p>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio(
        "Módulos Operativos",
        ["📊 Dashboard / KPIs", "📦 Inventario (Carga)", "🛒 Ventas (Facturar)", "💸 Gastos", "👥 Contactos", "⚙️ Configuración"]
    )

# =====================================================================
# MÓDULO 1: DASHBOARD INTELIGENTE Y MEDICIONES KPI
# =====================================================================
if menu == "📊 Dashboard / KPIs":
    st.markdown("## 📊 CONTROL GERENCIAL Y MEDIDORES KPI")
    
    # Lectura financiera del cono monetario consolidado
    conn = sqlite3.connect('gc_ecosistema_data_v4.db')
    ventas_df = pd.read_sql_query("SELECT SUM(total_ves) as total_ves, SUM(equivalente_usd) as total_usd, SUM(comision_ganada_usd) as comision FROM ventas", conn)
    conn.close()
    
    acumulado_ves = ventas_df['total_ves'].iloc[0] or 0.0
    acumulado_usd = ventas_df['total_usd'].iloc[0] or 0.0
    acumulado_comision = ventas_df['comision'].iloc[0] or 0.0
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(label="Tasa BCV Oficial (Referencial)", value=f"Bs. {cfg['tasa_bcv']:.5f}")
    with c2: st.metric(label="Ventas en Moneda Legal (VES)", value=f"Bs. {acumulado_ves:,.2f}")
    with c3: st.metric(label="Contravalor Ref. Almacén (USD)", value=f"${acumulado_usd:,.2f} USD")
    with c4: st.metric(label="Total Comisiones Vendedores", value=f"${acumulado_comision:,.2f} USD")

    st.write("---")
    
    col_izq, col_der = st.columns(2)
    with col_izq:
        st.write("**Volumen de Ventas por Operador Financiero (VES)**")
        conn = sqlite3.connect('gc_ecosistema_data_v4.db')
        df_vendedores = pd.read_sql_query("SELECT vendedor, SUM(total_ves) as Total FROM ventas GROUP BY vendedor", conn)
        conn.close()
        if df_vendedores.empty:
            df_vendedores = pd.DataFrame({'vendedor': ['Sin Operaciones'], 'Total': [0.0]})
        st.bar_chart(data=df_vendedores, x='vendedor', y='Total', color=cfg['color_marca'])
        
    with col_der:
        st.write("**Margen de Contribución por Canal Financiero**")
        st.dataframe(pd.DataFrame({
            'Canal de Distribución': ['Venta al Detal (Minorista)', 'Despacho por Caja/Bulto', 'Volumen Mayorista'],
            'Margen de Utilidad Promedio': ['25.00% - 30.00%', '15.00% - 18.00%', '10.00% - 12.00%'],
            'Estatus de Cumplimiento': ['✅ Óptimo', '✅ Óptimo', '✅ Regulado']
        }), hide_index=True, use_container_width=True)

    st.write("---")
    
    # Matrices Analíticas de Rotación y Módulo de Ofertas Flash
    st.markdown("### 🗂️ MONITOREO DE ROTACIÓN Y PRODUCTOS HUESO")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown("<p style='font-weight:bold; margin-bottom:5px;'>TOP PRODUCTOS MÁS DESPACHADOS</p>", unsafe_allow_html=True)
        conn = sqlite3.connect('gc_ecosistema_data_v4.db')
        top_prod_df = pd.read_sql_query("SELECT i.nombre as Producto, SUM(v.cantidad) as 'Bultos Vendidos' FROM ventas v JOIN inventario i ON v.codigo_producto = i.id GROUP BY i.nombre ORDER BY 'Bultos Vendidos' DESC LIMIT 5", conn)
        conn.close()
        if top_prod_df.empty:
            top_prod_df = pd.DataFrame({'Producto': ['No se registran facturas'], 'Bultos Vendidos': [0]})
        st.dataframe(top_prod_df, use_container_width=True, hide_index=True)

    with m2:
        st.markdown("<p style='font-weight:bold; margin-bottom:5px;'>ESTRUCTURA DE MÁRGENES ESTABLECIDOS</p>", unsafe_allow_html=True)
        conn = sqlite3.connect('gc_ecosistema_data_v4.db')
        df_margen = pd.read_sql_query("SELECT nombre as Producto, porc_ganancia as 'Margen %' FROM inventario ORDER BY porc_ganancia DESC LIMIT 5", conn)
        conn.close()
        st.dataframe(df_margen, use_container_width=True, hide_index=True)

    with m3:
        st.markdown("<p style='color:#e67e22; font-weight:bold; margin-bottom:5px;'>⚠️ ALERTAS BAJA ROTACIÓN (HUESO)</p>", unsafe_allow_html=True)
        conn = sqlite3.connect('gc_ecosistema_data_v4.db')
        df_hueso = pd.read_sql_query("SELECT id, nombre, stock, dias_stock FROM inventario WHERE dias_stock >= 15", conn)
        conn.close()
        
        if df_hueso.empty:
            st.info("Almacenes en perfecto equilibrio de rotación.")
        else:
            for idx, row in df_hueso.iterrows():
                col_t, col_b = st.columns(2)
                with col_t:
                    st.write(f"📦 **{row['nombre']}**  \nStock: {row['stock']} | Días: {row['dias_stock']}")
