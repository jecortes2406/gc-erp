import streamlit as st
import sqlite3

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="GC ERP Pro", layout="wide")
TASA_ANCLA_USDT = 45.0  # Ajustable desde aquí

# Inicializar Base de Datos
conn = sqlite3.connect('gc_erp.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS inventario 
             (id INTEGER PRIMARY KEY, nombre TEXT, precio_bulto REAL, precio_mayor REAL, precio_detal REAL, iva REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS ventas 
             (id INTEGER PRIMARY KEY, quiosco TEXT, monto_usdt REAL, comision_vendedor REAL)''')
conn.commit()

# --- MÓDULOS DEL SISTEMA ---
menu = st.sidebar.selectbox("Seleccione Módulo", ["Dashboard", "Inventario y Carga", "Ventas", "Comisiones"])

if menu == "Inventario y Carga":
    st.header("📦 Carga de Productos e Inventario")
    nombre = st.text_input("Nombre del Producto")
    bulto = st.number_input("Precio por Bulto (USDT)")
    mayor = st.number_input("Precio al Mayor (USDT)")
    detal = st.number_input("Precio al Detal (USDT)")
    iva_porc = st.slider("IVA (%)", 0, 16, 16)
    
    if st.button("Guardar Producto"):
        c.execute("INSERT INTO inventario (nombre, precio_bulto, precio_mayor, precio_detal, iva) VALUES (?,?,?,?,?)", 
                  (nombre, bulto, mayor, detal, iva_porc))
        conn.commit()
        st.success(f"Producto {nombre} cargado con éxito.")

elif menu == "Ventas":
    st.header("🛒 Módulo de Ventas")
    # Lógica de venta
    precio_final = st.number_input("Precio de Venta (USDT)", min_value=0.0)
    iva = st.number_input("IVA Aplicado (%)", 16)
    vendedor_pct = st.number_input("Comisión Vendedor (%)", 5)
    
    if st.button("Registrar Venta"):
        monto_con_iva = precio_final * (1 + (iva/100))
        comision = precio_final * (vendedor_pct/100)
        c.execute("INSERT INTO ventas (monto_usdt, comision_vendedor) VALUES (?,?)", (monto_con_iva, comision))
        conn.commit()
        st.write(f"Total Cliente (con IVA): {monto_con_iva * TASA_ANCLA_USDT} VES")
        st.info(f"Comisión calculada para vendedor: {comision:.2f} USDT")

elif menu == "Comisiones":
    st.header("💰 Liquidación de Comisiones")
    df = pd.read_sql("SELECT * FROM ventas", conn)
    st.dataframe(df)
    st.metric("Total a pagar en comisiones", f"{df['comision_vendedor'].sum():.2f} USDT")
