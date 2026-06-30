import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse

# =====================================================================
# MOTOR DE INICIALIZACIÓN Y AUTO-MIGRACIÓN DE BASE DE DATOS
# =====================================================================
def inicializar_estructura_saint_erp():
    conn = sqlite3.connect('gc_saint_ecosistema.db')
    cursor = conn.cursor()
    
    # 1. Configuración de Marca y Parámetros Cambiarios (Módulo Central)
    cursor.execute('''CREATE TABLE IF NOT EXISTS configuracion (
                        id INTEGER PRIMARY KEY, nombre_empresa TEXT, color_marca TEXT,
                        tasa_bcv REAL, tasa_euro REAL, tasa_binance REAL, comision_vendedor_porc REAL)''')
    
    # 2. Archivo: Depósitos (Ubicaciones Físicas de Mercancía)
    cursor.execute('''CREATE TABLE IF NOT EXISTS depositos (
                        codigo TEXT PRIMARY KEY, descripcion TEXT, responsable TEXT)''')
    
    # 3. Archivo: Instancias de Inventario (Departamentos / Grupos de Productos)
    cursor.execute('''CREATE TABLE IF NOT EXISTS instancias (
                        codigo TEXT PRIMARY KEY, descripcion TEXT)''')
    
    # 4. Archivo: Maestro de Inventario (Artículos y Servicios Diferenciados)
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
                        id TEXT PRIMARY KEY, nombre TEXT, tipo_item TEXT, instancia_cod TEXT,
                        deposito_cod TEXT, costo_usd REAL, porc_ganancia REAL, precio_detal_ves REAL, 
                        precio_caja_ves REAL, precio_mayor_ves REAL, lote_zeta TEXT, stock INTEGER, 
                        dias_stock TEXT, tipo_impuesto TEXT, manejo_decimales INTEGER, marca TEXT, referencia TEXT)''')
    
    # 5. Archivo: Directorio de Clientes y Proveedores (Contribuyentes Especiales / Retenciones)
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        rif_cedula TEXT PRIMARY KEY, nombre TEXT, telefono TEXT, direccion TEXT, contribuyente_especial INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
                        rif TEXT PRIMARY KEY, empresa TEXT, telefono TEXT, contacto TEXT, contribuyente_especial INTEGER)''')
    
    # 6. Transacciones: Libro Diario de Ventas, Egresos e Instrumentos de Pago
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, tipo_documento TEXT, estatus TEXT,
                        cliente_id TEXT, vendedor TEXT, codigo_producto TEXT, cantidad REAL, precio_aplicado_ves REAL, subtotal_ves REAL, 
                        iva_ves REAL, igtf_ves REAL, total_ves REAL, equivalente_usd REAL, 
                        comision_ganada_usd REAL, instrumento_pago TEXT, estatus_fiscal TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, descripcion TEXT, monto_original REAL, 
                        moneda TEXT, tasa_cambio REAL, equivalente_usd REAL, proveedor_rif TEXT)''')

    # Inyectar configuraciones basales de Saint Enterprise si el sistema está vacío
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO configuracion VALUES (1, 'Grupo Comercial, C.A.', '#1B4F72', 45.50633, 49.33210, 47.85350, 5.0)")
        
    cursor.execute("SELECT COUNT(*) FROM depositos")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO depositos VALUES ('01', 'Depósito Principal Almacén', 'Responsable de Almacén')")
        cursor.execute("INSERT INTO depositos VALUES ('02', 'Depósito Auxiliar de Tienda', 'Supervisor de Turno')")
        
    cursor.execute("SELECT COUNT(*) FROM instancias")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO instancias VALUES ('VIV', 'Víveres Surtidos')")
        cursor.execute("INSERT INTO instancias VALUES ('LIM', 'Limpieza General')")
        cursor.execute("INSERT INTO instancias VALUES ('LIC', 'Licores Nacionales e Importados')")
        
    cursor.execute("SELECT COUNT(*) FROM inventario")
    if cursor.fetchone() == 0:
        cursor.execute("INSERT INTO inventario VALUES ('01001', 'BIANCHI CARAMELO CHOCOLATE 18BX100U', 'Artículo', 'VIV', '01', 30.00, 25.00, 1740.00, 1600.00, 1550.00, 'Z-101', 183, 'Alta', 'Exento', 0, 'Mari', '01001')")
        cursor.execute("INSERT INTO inventario VALUES ('01002', 'QUESO BLANCO DURO SANTA BÁRBARA', 'Artículo', 'VIV', '01', 5.00, 30.00, 295.00, 280.00, 270.00, 'Z-Lácteos', 45, 'Hueso', 'Exento', 1, 'Local', '01002')")
        cursor.execute("INSERT INTO clientes VALUES ('J-123456780', 'Distribuidora Surtidora Central, C.A.', '584121234567', 'Caracas, Distrito Capital', 1)")
        cursor.execute("INSERT INTO proveedores VALUES ('J-999999990', 'Confiterías El Bulto Mayorista', '584149876543', 'Maracay Almacenes', 0)")
        
    conn.commit()
    conn.close()

inicializar_estructura_saint_erp()

# Extraer parámetros de configuración globales de la base de datos
conn = sqlite3.connect('gc_saint_ecosistema.db')
cfg = pd.read_sql_query("SELECT * FROM configuracion WHERE id=1", conn).iloc
conn.close()

# Configuración de página de Streamlit
st.set_page_config(page_title=f"{cfg['nombre_empresa']} - Saint Enterprise Administrativo", layout="wide", page_icon="🏢")

# Estilos CSS de Alta Definición y Lectura Ejecutiva (Fondo Claro, Textos Oscuros)
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
        div.stDataFrame {{ background-color: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; }}
    </style>
""", unsafe_allow_html=True)

# --- MENÚ LATERAL IZQUIERDO ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom:0;'>GC</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-weight: bold; font-size:12px;'>{cfg['nombre_empresa'].upper()}<br><small style='color:#e67e22;'>SAINT ADMINISTRATIVE WEB</small></p>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio(
        "Módulos Operativos (Archivos)",
        ["📊 Panel de Inicio / KPIs", "📦 Ficha de Inventario", "🚚 Compras y Proveedores", "🛒 Facturación de Ventas", "💸 Egresos / Caja Chica", "⚙️ Configuración Global"]
    )

# =====================================================================
# MÓDULO 1: PANEL DE INICIO / KPIs
# =====================================================================
if menu == "📊 Panel de Inicio / KPIs":
    st.markdown("## 📊 CONTROL GERENCIAL Y MEDIDORES KPI")
    
    conn = sqlite3.connect('gc_saint_ecosistema.db')
    ventas_df = pd.read_sql_query("SELECT SUM(total_ves) as total_ves, SUM(equivalente_usd) as total_usd, SUM(comision_ganada_usd) as comision FROM ventas WHERE estatus='Facturado'", conn)
    conn.close()
    
    acumulado_ves = ventas_df['total_ves'].iloc if not ventas_df.empty and ventas_df['total_ves'].iloc is not None else 0.0
    acumulado_usd = ventas_df['total_usd'].iloc if not ventas_df.empty and ventas_df['total_usd'].iloc is not None else 0.0
    acumulado_comision = ventas_df['comision'].iloc if not ventas_df.empty and ventas_df['comision'].iloc is not None else 0.0
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(label="Tasa BCV Referencial", value=f"Bs. {cfg['tasa_bcv']:.5f}")
    with c2: st.metric(label="Ventas en Moneda Legal (VES)", value=f"Bs. {acumulado_ves:,.2f}")
    with c3: st.metric(label="Contravalor Ref. Almacén (USD)", value=f"${acumulado_usd:,.2f} USD")
    with c4: st.metric(label="Total Comisiones Turno", value=f"${acumulado_comision:,.2f} USD")

    st.write("---")
    
    col_izq, col_der = st.columns(2)
    with col_izq:
        st.write("**Rendimiento del Equipo de Ventas (VES)**")
        conn = sqlite3.connect('gc_saint_ecosistema.db')
        df_vendedores = pd.read_sql_query("SELECT vendedor, SUM(total_ves) as Total FROM ventas WHERE estatus='Facturado' GROUP BY vendedor", conn)
        conn.close()
        if df_vendedores.empty:
            df_vendedores = pd.DataFrame({'vendedor': ['Bolsas Surtidas', 'Choco Surtido', 'Trululu Aros', 'Gomas Menta', 'Lokiño Barra', 'Caramelo Choc'], 'Total': [450.0, 320.0, 610.0, 150.0, 290.0, 410.0]})
        st.bar_chart(data=df_vendedores, x='vendedor', y='Total', color=cfg['color_marca'])
        
    with col_der:
        st.write("**⚠️ PRODUCTOS CON BAJA ROTACIÓN (HUESO) - ACCIONES DIRECTAS**")
        conn = sqlite3.connect('gc_saint_ecosistema.db')
        df_hueso = pd.read_sql_query("SELECT id, nombre, stock, dias_stock FROM inventario WHERE dias_stock = 'Hueso'", conn)
        conn.close()
        
        if df_hueso.empty:
            st.info("Almacenes en perfecto equilibrio de rotación continua.")
        else:
            for idx, row in df_hueso.iterrows():
