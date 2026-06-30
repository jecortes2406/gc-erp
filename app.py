import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse

# =====================================================================
# MOTOR DE INICIALIZACIÓN Y AUTO-MIGRACIÓN DE BASE DE DATOS CONTABLE
# =====================================================================
def inicializar_estructura_erp():
    conn = sqlite3.connect('gc_ecosistema_data_v5.db')
    cursor = conn.cursor()
    
    # 1. Configuración de Marca, Agencias y Parámetros Cambiarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS configuracion (
                        id INTEGER PRIMARY KEY, nombre_empresa TEXT, color_marca TEXT,
                        tasa_bcv REAL, tasa_euro REAL, tasa_binance REAL, comision_vendedor_porc REAL)''')
    
    # 2. Maestro de Inventario Avanzado con Control de Kardex y Tipo (Artículo/Servicio)
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
                        id INTEGER PRIMARY KEY, nombre TEXT, tipo TEXT, costo_usd REAL, porc_ganancia REAL,
                        precio_detal_ves REAL, precio_caja_ves REAL, precio_mayor_ves REAL,
                        lote_zeta TEXT, stock INTEGER, dias_stock INTEGER, rotacion TEXT)''')
    
    # 3. Registro Operativo de Documentos de Ventas (Facturas, Cotizaciones, Notas de Entrega)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, tipo_documento TEXT, estatus TEXT,
                        cliente_id TEXT, vendedor TEXT, codigo_producto INTEGER, cantidad INTEGER, 
                        precio_aplicado_ves REAL, subtotal_ves REAL, iva_ves REAL, igtf_ves REAL, 
                        total_ves REAL, equivalente_usd REAL, comision_ganada_usd REAL, forma_pago TEXT, moneda TEXT)''')
    
    # 4. Directorio de Contactos (Clientes y Proveedores)
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (rif_cedula TEXT PRIMARY KEY, nombre TEXT, telefono TEXT, direccion TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (rif TEXT PRIMARY KEY, empresa TEXT, telefono TEXT, contacto TEXT)''')
    
    # 5. Libro de Compras y Egresos Multimoneda
    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, descripcion TEXT,
                        monto_original REAL, moneda TEXT, tasa_cambio REAL, equivalente_usd REAL, proveedor_rif TEXT)''')
    
    # Inyectar muestras comerciales iniciales de confitería si el sistema está nuevo
    cursor.execute("SELECT COUNT(*) FROM configuracion")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO configuracion VALUES (1, 'Grupo Comercial, C.A.', '#1B4F72', 45.50633, 49.33210, 47.85350, 5.0)")
    
    cursor.execute("SELECT COUNT(*) FROM inventario")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO inventario VALUES (1061, 'BIANCHI CARAMELO CHOCOLATE 18BX100U', 'Artículo', 30.00, 25.00, 1740.00, 1600.00, 1550.00, 'Z-101', 183, 0, 'Alta')")
        cursor.execute("INSERT INTO inventario VALUES (1092, 'TRULULU AROS 36BX50U (HUESO)', 'Artículo', 50.00, 30.00, 3020.00, 2800.00, 2700.00, 'Z-Hueso', 38, 29, 'Hueso')")
        cursor.execute("INSERT INTO clientes VALUES ('J-123456780', 'Distribuidora Surtidora Central, C.A.', '584121234567', 'Caracas, Distrito Capital')")
        cursor.execute("INSERT INTO proveedores VALUES ('J-999999990', 'Confiterías El Bulto Mayorista', '584149876543', 'Maracay Almacenes')")
    
    conn.commit()
    conn.close()

inicializar_estructura_erp()

# Extraer parámetros de configuración globales guardados
conn = sqlite3.connect('gc_ecosistema_data_v5.db')
cfg = pd.read_sql_query("SELECT * FROM configuracion WHERE id=1", conn).iloc[0]
conn.close()

# Configuración de página de Streamlit
st.set_page_config(page_title=f"{cfg['nombre_empresa']} - Administrative Business Web ERP", layout="wide", page_icon="🏢")

# Inyección de Estilos CSS Profesionales (Fondo Claro, Alta Definición y Lectura Ejecutiva)
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

# --- MENÚ LATERAL IZQUIERDO (SIDEBAR ADMINISTRATIVO) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom:0;'>GC</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-weight: bold; font-size:12px;'>{cfg['nombre_empresa'].upper()}<br><small style='color:#e67e22;'>ADMINISTRATIVE WEB ERP</small></p>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio(
        "Módulos del Sistema",
        ["📊 Panel de Inicio", "📦 Inventario (Artículos)", "🚚 Módulo de Compras", "🛒 Facturación y Ventas", "💸 Egresos / Caja Chica", "⚙️ Configuración Global"]
    )

# =====================================================================
# MÓDULO 1: PANEL DE INICIO (KPIs Y ESTADÍSTICAS EN LA NUBE)
# =====================================================================
if menu == "📊 Panel de Inicio":
    st.markdown("## 📊 CONTROL GERENCIAL Y MEDIDORES KPI")
    
    conn = sqlite3.connect('gc_ecosistema_data_v5.db')
    ventas_df = pd.read_sql_query("SELECT SUM(total_ves) as total_ves, SUM(equivalente_usd) as total_usd, SUM(comision_ganada_usd) as comision FROM ventas WHERE estatus='Facturado'", conn)
    conn.close()
    
    acumulado_ves = ventas_df['total_ves'].iloc[0] or 0.0
    acumulado_usd = ventas_df['total_usd'].iloc[0] or 0.0
    acumulado_comision = ventas_df['comision'].iloc[0] or 0.0
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric(label="Tasa BCV del Día (Moneda Legal)", value=f"Bs. {cfg['tasa_bcv']:.5f}")
    with c2: st.metric(label="Ventas en Moneda Legal (VES)", value=f"Bs. {acumulado_ves:,.2f}")
    with c3: st.metric(label="Contravalor Ref. Almacén (USD)", value=f"${acumulado_usd:,.2f} USD")
    with c4: st.metric(label="Total Comisiones Vendedores", value=f"${acumulado_comision:,.2f} USD")

    st.write("---")
    
    col_izq, col_der = st.columns(2)
    with col_izq:
        st.write("**Rendimiento del Equipo de Ventas (VES)**")
        conn = sqlite3.connect('gc_ecosistema_data_v5.db')
        df_vendedores = pd.read_sql_query("SELECT vendedor, SUM(total_ves) as Total FROM ventas WHERE estatus='Facturado' GROUP BY vendedor", conn)
        conn.close()
        if df_vendedores.empty:
            df_vendedores = pd.DataFrame({'vendedor': ['Cajero Inicial'], 'Total': [0.0]})
        st.bar_chart(data=df_vendedores, x='vendedor', y='Total', color=cfg['color_marca'])
        
    with col_der:
        st.write("**⚠️ PRODUCTOS CON BAJA ROTACIÓN (HUESO) - ACCIONES DIRECTAS**")
        conn = sqlite3.connect('gc_ecosistema_data_v5.db')
        df_hueso = pd.read_sql_query("SELECT id, nombre, stock, dias_stock FROM inventario WHERE dias_stock >= 15", conn)
        conn.close()
        
        if df_hueso.empty:
            st.info("Almacenes en perfecto equilibrio de rotación continua.")
        else:
            for idx, row in df_hueso.iterrows():
                col_t, col_b = st.columns([3, 1])
                with col_t:
                    st.write(f"📦 **{row['nombre']}** | Stock: {row['stock']} bultos | Parado: {row['dias_stock']} días")
                with col_b:
                    if st.button("PROMO", key=f"promo_{row['id']}"):
                        msg = f"🎉 *¡OFERTA FLASH DE LIQUIDACIÓN!* 🎉\n\nTenemos en promoción:\n📦 *{row['nombre']}*\n⚡ ¡Escríbenos para aplicar tarifa de remate corporativo!"
                        link = f"https://whatsapp.com{urllib.parse.quote(msg)}"
                        st.markdown(f"[📲 Enviar]({link})")

# =====================================================================
# MÓDULO 2: INVENTARIO (ARTÍCULOS Y CONTROL DE KARDEX CONTINUO)
# =====================================================================
elif menu == "📦 Inventario (Artículos)":
    st.markdown("## 📦 CONTROL DE INVENTARIO Y FICHA DE ARTÍCULOS")
    
    with st.form("form_inventario", clear_on_submit=True):
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            id_sku = st.number_input("Código SKU Correlativo", min_value=1000, max_value=9999, value=1100)
            nombre = st.text_input("Descripción del Artículo / Servicio", placeholder="Ej: LOKIÑO CARAMELO 24BX100U")
            tipo_item = st.selectbox("Tipo de Ítem", ["Artículo", "Servicio"])
        with cc2:
            costo_usd = st.number_input("Costo de Adquisición (USD por Bulto)", min_value=0.0, format="%.2f")
            ganancia_porc = st.number_input("% Margen de Utilidad Neto", min_value=0.0, max_value=100.0, value=30.0)
            lote = st.text_input("Número de Lote (Zeta)", placeholder="Ej: Z-2026")
        with cc3:
