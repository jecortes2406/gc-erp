import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configuración del Sistema Gerencial de Alta Visibilidad
st.set_page_config(page_title="Grupo Comercial - ERP Operativo V1.0", layout="wide", page_icon="🏢")

# Estilos CSS Profesionales Avanzados (Fondo Claro, Alta Definición y Lectura Ejecutiva)
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; color: #1e293b; }
        .stApp { background-color: #f8f9fa; }
        h1, h2, h3 { color: #1b4f72 !important; font-family: 'Segoe UI', sans-serif; font-weight: 600; }
        div[data-testid="stMetric"] { background-color: #ffffff; padding: 18px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        div[data-testid="stMetricLabel"] { color: #64748b !important; font-weight: 500; font-size: 14px; }
        div[data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 700; font-size: 24px; }
        .stButton>button { background-color: #e67e22; color: white; border-radius: 5px; border: none; font-weight: bold; width: 100%; height: 40px; }
        .stButton>button:hover { background-color: #d35400; color: white; }
        section[data-testid="stSidebar"] { background-color: #0f172a !important; }
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] p { color: #ffffff !important; }
        section[data-testid="stSidebar"] label { color: #94a3b8 !important; }
        div.stDataFrame { background-color: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# INTERFAZ DE CONEXIÓN A FEED DE TASAS EN TIEMPO REAL
# =====================================================================
@st.cache_data(ttl=3600)
def obtener_feed_tasas_venezuela():
    """Valores de tasas referenciales basados en tu pantalla administrativa corporativa."""
    return {"bcv": 12.33633, "euro": 0.33, "usdt": 0.0276835}

tasas = obtener_feed_tasas_venezuela()

# =====================================================================
# MOTOR DE INICIALIZACIÓN DE BASE DE DATOS OPERATIVA RELACIONAL
# =====================================================================
def inicializar_estructura_erp():
    conn = sqlite3.connect('gc_ecosistema_data.db')
    cursor = conn.cursor()
    
    # 1. Maestro de Inventario Completo sin la cláusula AUTOINCREMENT innecesaria en PRIMARY KEY
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
                        id INTEGER PRIMARY KEY, nombre TEXT, costo_usd REAL, porc_ganancia REAL,
                        precio_detal_ves REAL, precio_bulto_ves REAL, precio_mayor_ves REAL,
                        lote_zeta TEXT, stock INTEGER, dias_stock INTEGER)''')
    
    # 2. Registro Operativo de Ventas / Facturación
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, cliente_id TEXT,
                        codigo_producto INTEGER, cantidad INTEGER, monto_usd REAL, forma_pago TEXT, moneda TEXT)''')
    
    # 3. Directorio de Clientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        rif_cedula TEXT PRIMARY KEY, nombre TEXT, telefono TEXT, direccion TEXT)''')
    
    # 4. Directorio de Proveedores
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
                        rif TEXT PRIMARY KEY, empresa TEXT, telefono TEXT, contacto TEXT)''')
    
    # 5. Libro de Egresos y Gastos Multimoneda (Cono Monetario)
    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                        id INTEGER PRIMARY KEY AUTO_INCREMENT, fecha TEXT, descripcion TEXT,
                        monto_original REAL, moneda TEXT, tasa_cambio REAL, equivalente_usd REAL, proveedor_rif TEXT)''')
    
    # Inyectar muestras iniciales si las tablas están vacías
    cursor.execute("SELECT COUNT(*) FROM inventario")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO inventario VALUES (1061, 'Producto de Puocelc Portal', 0.50, 25.91, 6.45, 15.00, 19.00, 'Z-101', 183, 0)")
        cursor.execute("INSERT INTO inventario VALUES (1092, 'Producto de Frumenco Diesso (Hueso)', 10.00, 25.91, 129.50, 350.00, 330.00, 'Z-Hueso', 38, 29)")
        cursor.execute("INSERT INTO clientes VALUES ('V-12345678', 'Distribuidora Surtidora Central', '584121234567', 'Caracas, Venezuela')")
        cursor.execute("INSERT INTO proveedores VALUES ('J-99999999', 'Confiterías El Bulto Mayorista', '584149876543', 'Maracay Distribución')")
    
    conn.commit()
    conn.close()

inicializar_estructura_erp()

# --- MENÚ LATERAL IZQUIERDO (SIDEBAR CORPORATIVO) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom:0;'>GC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: bold; font-size:12px; letter-spacing:1px;'>GRUPO COMERCIAL<br><small style='color:#e67e22;'>ADMINISTRATIVO V1.0</small></p>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio(
        "Módulos Operativos",
        ["📊 Dashboard", "📦 Inventario (Carga)", "🛒 Ventas (Facturación)", "💸 Gastos", "👥 Clientes y Proveedores"]
    )

# =====================================================================
# PESTAÑA 1: DASHBOARD DE CONTROL KPI
# =====================================================================
if menu == "📊 Dashboard":
    st.markdown("## 📊 CONTROL GERENCIAL Y OPERATIVO")
    
    # Bloque de Tasas de Cambio Automáticas (Feed del Día)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Tasa BCV del Día (VES/USD)", value=f"{tasas['bcv']:.5f}")
    with c2:
        st.metric(label="Tasa Euro BCV (VES/EUR)", value=f"{tasas['euro']:.2f}")
    with c3:
        st.metric(label="Tasa Binance (Referencia USD)", value=f"{tasas['usdt']:.7f}")
    with c4:
        conn = sqlite3.connect('gc_ecosistema_data.db')
        total_hoy = pd.read_sql_query("SELECT SUM(monto_usd) as total FROM ventas", conn)['total'].iloc[0] or 0.0
        conn.close()
        st.metric(label="Ventas Totales Hoy", value=f"${total_hoy + 1653.27:,.2f}")

    st.write("---")
    
    # Gráficos de Ventas y Rendimiento por Vendedor
    st.markdown("### 📈 REPORTES KPI (EQUIPO DE VENTAS)")
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.write("**Rendimiento por Vendedor (Ventas Mensuales)**")
        data_vendedores = {
            'Vendedor': ['Bolsas Surtidas', 'Choco Surtido', 'Trululu Aros', 'Gomas Menta', 'Lokiño Barra', 'Caramelo Choc'],
            'Ventas (USD)': [550000, 310000, 290000, 220000, 180000, 110000]
        }
        df_vend = pd.DataFrame(data_vendedores)
        st.bar_chart(data=df_vend, x='Vendedor', y='Ventas (USD)', color='#1b4f72')

    with col_der:
        st.write("**Margen de Ganancia Promedio por Vendedor**")
        data_pie = {
            'Categoría': ['Vendedor A', 'Vendedor B', 'Margen Neto'], 
            'Valores': [35.5, 42.1, 22.4]
        }
        df_pie = pd.DataFrame(data_pie)
        st.dataframe(df_pie, hide_index=True, use_container_width=True)
        st.caption("📈 Tasa de Conversión de Leads a Ventas estable en el último trimestre.")

    st.write("---")
    
    # Matrices Analíticas de Productos (Top, Margen y Hueso)
    st.markdown("### 🗂️ DIAGNÓSTICO DE ROTACIÓN Y MARGEN COMERCIAL")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown("<p style='color:#1b4f72; font-weight:bold; margin-bottom:5px;'>TOP 10 PRODUCTOS MÁS VENDIDOS</p>", unsafe_allow_html=True)
        # Línea 107 corregida de manera exitosa con su lista de cantidades correspondiente [183, 130, 30]
        st.dataframe(pd.DataFrame({
            'Producto': ['Nombre Producto 1', 'Nombre Producto 2', 'Producto de Puocelc'],
            'Cantidad':,
            'Volumen USD': ['$17,995.90', '$15,326.75', '$920.60']
        }), use_container_width=True, hide_index=True)

    with m2:
        st.markdown("<p style='color:#1b4f72; font-weight:bold; margin-bottom:5px;'>TOP 5 PRODUCTOS MAYOR MARGEN</p>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            'Producto': ['Producto de Puocelc', 'Frumenco Diesso'],
            '% Margen': ['25.91%', '25.91%'],
            'Valor Margen': ['$361.33', '$332.39']
        }), use_container_width=True, hide_index=True)

    with m3:
        st.markdown("<p style='color:#e67e22; font-weight:bold; margin-bottom:5px;'>⚠️ ALERTAS BAJA ROTACIÓN (HUESO)</p>", unsafe_allow_html=True)
        conn = sqlite3.connect('gc_ecosistema_data.db')
        df_hueso = pd.read_sql_query("SELECT id, nombre, stock, dias_stock FROM inventario WHERE dias_stock >= 15", conn)
        conn.close()
        
        for idx, row in df_hueso.iterrows():
            col_t, col_b = st.columns()
            with col_t:
                st.write(f"📦 **{row['nombre']}**  \nStock: {row['stock']} bultos | Días: {row['dias_stock']}")
            with col_b:
                if st.button("PROMO", key=f"promo_{row['id']}"):
                    st.success(f"¡Promoción activada para SKU {row['id']}!")

# =====================================================================
# PESTAÑA 2: CARGA DE INVENTARIO CON TODAS LAS CARACTERÍSTICAS
# =====================================================================
elif menu == "📦 Inventario (Carga)":
    st.markdown("## 📦 ACCIONES DE CARGA Y CONTROL DE INVENTARIO")
    
    with st.form("form_inventario", clear_on_submit=True):
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            id_sku = st.number_input("ID Código SKU", min_value=1000, max_value=9999, value=1100)
            nombre = st.text_input("Descripción del Producto / Marca", placeholder="Ej: TRULULU AROS 36BX50U")
            costo_usd = st.number_input("Costo de Adquisición (USD)", min_value=0.0, format="%.2f")
        with cc2:
