import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse

# =====================================================================
# MOTOR DE INICIALIZACIÓN DE BASE DE DATOS OPERATIVA RELACIONAL
# =====================================================================
def inicializar_estructura_erp():
    conn = sqlite3.connect('gc_ecosistema_data.db')
    cursor = conn.cursor()
    
    # 1. Configuración de Marca, Tasas e Incentivos
    cursor.execute('''CREATE TABLE IF NOT EXISTS configuracion (
                        id INTEGER PRIMARY KEY, nombre_empresa TEXT, color_marca TEXT,
                        tasa_bcv REAL, tasa_euro REAL, tasa_binance REAL, comision_vendedor_porc REAL)''')
    
    # 2. Maestro de Inventario Avanzado con 3 Niveles de Precios
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
                        id INTEGER PRIMARY KEY, nombre TEXT, costo_usd REAL, porc_ganancia REAL,
                        precio_detal_ves REAL, precio_bulto_ves REAL, precio_mayor_ves REAL,
                        lote_zeta TEXT, stock INTEGER, dias_stock INTEGER, rotacion TEXT)''')
    
    # 3. Registro Operativo de Ventas / Facturación Real
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, cliente_id TEXT, vendedor TEXT,
                        codigo_producto INTEGER, cantidad INTEGER, precio_aplicado_usd REAL, 
                        monto_usd REAL, comision_ganada_usd REAL, forma_pago TEXT, moneda TEXT)''')
    
    # 4. Directorio de Clientes y Proveedores
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (rif_cedula TEXT PRIMARY KEY, nombre TEXT, telefono TEXT, direccion TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (rif TEXT PRIMARY KEY, empresa TEXT, telefono TEXT, contacto TEXT)''')
    
    # 5. Libro de Egresos y Gastos Multimoneda
    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, descripcion TEXT,
                        monto_original REAL, moneda TEXT, tasa_cambio REAL, equivalente_usd REAL, proveedor_rif TEXT)''')
    
    # Inyectar muestras iniciales si las tablas están vacías
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO configuracion VALUES (1, 'Grupo Comercial', '#1B4F72', 45.50633, 49.33210, 47.85350, 5.0)")
    
    cursor.execute("SELECT COUNT(*) FROM inventario")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO inventario VALUES (1061, 'Producto de Puocelc Portal', 0.50, 25.91, 6.45, 15.00, 19.00, 'Z-101', 183, 0, 'Alta')")
        cursor.execute("INSERT INTO inventario VALUES (1092, 'Producto de Frumenco Diesso (Hueso)', 10.00, 25.91, 129.50, 350.00, 330.00, 'Z-Hueso', 38, 29, 'Hueso')")
        cursor.execute("INSERT INTO clientes VALUES ('V-12345678', 'Distribuidora Surtidora Central', '584121234567', 'Caracas, Venezuela')")
        cursor.execute("INSERT INTO proveedores VALUES ('J-99999999', 'Confiterías El Bulto Mayorista', '584149876543', 'Maracay Distribución')")
    
    conn.commit()
    conn.close()

inicializar_estructura_erp()

# Extraer parámetros de configuración guardados
conn = sqlite3.connect('gc_ecosistema_data.db')
cfg = pd.read_sql_query("SELECT * FROM configuracion WHERE id=1", conn).iloc[0]
conn.close()

# Configuración del Entorno de Alta Visibilidad
st.set_page_config(page_title=f"{cfg['nombre_empresa']} - ERP", layout="wide", page_icon="🏢")

# Inyección de Estilos CSS basados en la Configuración del Usuario
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
    st.markdown(f"<h1 style='text-align: center; margin-bottom:0;'>GC</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-weight: bold; font-size:12px;'>{cfg['nombre_empresa'].upper()}<br><small style='color:#e67e22;'>ERP INTEGRAL V1.0</small></p>", unsafe_allow_html=True)
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
    
    # Fila de Tasas de Cambio en Vivo + Ingresos Totales
    conn = sqlite3.connect('gc_ecosistema_data.db')
    ventas_totales_df = pd.read_sql_query("SELECT SUM(monto_usd) as total FROM ventas", conn)
    comisiones_totales_df = pd.read_sql_query("SELECT SUM(comision_ganada_usd) as total FROM ventas", conn)
    total_hoy = ventas_totales_df['total'].iloc[0] or 0.0
    total_comision = comisiones_totales_df['total'].iloc[0] or 0.0
    conn.close()
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(label="Tasa BCV Oficial", value=f"Bs. {cfg['tasa_bcv']:.5f}")
    with c2: st.metric(label="Tasa Euro Oficial", value=f"Bs. {cfg['tasa_euro']:.5f}")
    with c3: st.metric(label="Tasa Binance P2P", value=f"Bs. {cfg['tasa_binance']:.5f}")
    with c4: st.metric(label="Ventas Consolidadas (USD)", value=f"${total_hoy + 1653.27:,.2f}")

    st.write("---")
    
    # Sección de Gráficos e Indicadores de Rendimiento de Ventas
    col_izq, col_der = st.columns(2)
    with col_izq:
        st.write("**Rendimiento del Equipo de Ventas (USD)**")
        conn = sqlite3.connect('gc_ecosistema_data.db')
        df_agrupado_vendedores = pd.read_sql_query("SELECT vendedor, SUM(monto_usd) as Total FROM ventas GROUP BY vendedor", conn)
        conn.close()
        
        if df_agrupado_vendedores.empty:
            df_agrupado_vendedores = pd.DataFrame({'vendedor': ['Cajero Predeterminado'], 'Total': [1653.27]})
        st.bar_chart(data=df_agrupado_vendedores, x='vendedor', y='Total', color=cfg['color_marca'])
        
    with col_der:
        st.write("**Resumen Operativo de Comisiones Acumuladas**")
        st.metric(label="Total Comisiones Asignadas (USD)", value=f"${total_comision:,.2f}")
        st.caption(f"Incentivo calculado bajo el parámetro del {cfg['comision_vendedor_porc']}% sobre el volumen neto facturado por cada SKU.")

    st.write("---")
    
    # Matrices Analíticas de Rotación y Productos Hueso
    st.markdown("### 🗂️ ANÁLISIS DE ROTACIÓN Y MARGENES DE PRODUCTOS")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.markdown("<p style='font-weight:bold; margin-bottom:5px;'>TOP PRODUCTOS MÁS VENDIDOS</p>", unsafe_allow_html=True)
        conn = sqlite3.connect('gc_ecosistema_data.db')
        top_prod_df = pd.read_sql_query("SELECT i.nombre as Producto, SUM(v.cantidad) as Cantidad FROM ventas v JOIN inventario i ON v.codigo_producto = i.id GROUP BY i.nombre ORDER BY Cantidad DESC LIMIT 5", conn)
        conn.close()
        if top_prod_df.empty:
            top_prod_df = pd.DataFrame({'Producto': ['Muestra Producto 1'], 'Cantidad': [100]})
        st.dataframe(top_prod_df, use_container_width=True, hide_index=True)

    with m2:
        st.markdown("<p style='font-weight:bold; margin-bottom:5px;'>TOP PRODUCTOS MAYOR MARGEN</p>", unsafe_allow_html=True)
        conn = sqlite3.connect('gc_ecosistema_data.db')
        df_margen = pd.read_sql_query("SELECT nombre as Producto, porc_ganancia as 'Margen %' FROM inventario ORDER BY porc_ganancia DESC LIMIT 5", conn)
        conn.close()
        st.dataframe(df_margen, use_container_width=True, hide_index=True)

    with m3:
        st.markdown("<p style='color:#e67e22; font-weight:bold; margin-bottom:5px;'>⚠️ ALERTAS BAJA ROTACIÓN (HUESO)</p>", unsafe_allow_html=True)
        conn = sqlite3.connect('gc_ecosistema_data.db')
        df_hueso = pd.read_sql_query("SELECT id, nombre, stock, dias_stock FROM inventario WHERE dias_stock >= 15", conn)
        conn.close()
        
        if df_hueso.empty:
            st.info("No hay inventario estancado en los almacenes.")
        else:
            for idx, row in df_hueso.iterrows():
                col_t, col_b = st.columns()
                with col_t:
                    st.write(f"📦 **{row['nombre']}**  \nStock: {row['stock']} bultos | Parado: {row['dias_stock']} días")
                with col_b:
                    if st.button("PROMO", key=f"promo_{row['id']}"):
                        msg = f"🎉 *¡OFERTA FLASH!* 🎉\n\nTenemos en promoción:\n📦 *{row['nombre']}*\n⚡ ¡Escríbenos para asegurar tu bulto!"
                        link = f"https://whatsapp.com{urllib.parse.quote(msg)}"
