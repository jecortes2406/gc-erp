import streamlit as st
import pandas as pd

# Configuración: El cliente nunca ve esta tasa, es tu "ancla" interna
TASAS_INTERNAS = {"USDT": 1.0, "VES": 45.0} # Ajusta tu tasa real aquí

st.set_page_config(page_title="GC ERP - Sistema Interno", layout="wide")

st.title("🛡️ GC ERP - Gestión Interna")

# MÓDULO DE VENTAS (Solo lógica interna)
st.subheader("Registrar Venta")
col1, col2 = st.columns(2)

with col1:
    quiosco = st.selectbox("Seleccionar Quiosco/Almacén", ["Quiosco 1", "Quiosco 2", "Almacén Central"])
with col2:
    monto_local = st.number_input("Monto total a cobrar al cliente (Moneda Local)", min_value=0.0)

# CÁLCULO DE EQUILIBRIO (Oculto al cliente)
if st.button("Procesar Venta Protegida"):
    # Convertimos a USDT internamente para el resguardo del valor
    monto_usdt = monto_local / TASAS_INTERNAS["VES"]
    
    st.info(f"Venta registrada en {quiosco}")
    st.write("---")
    st.caption("Resumen interno para Gerencia:")
    st.write(f"**Valor de resguardo (USDT):** {monto_usdt:.2f} USDT")
    st.success("Transacción exitosa. El cliente solo visualizó el monto en moneda local.")

# MÓDULO DE INVENTARIO (Estructura de 3 precios)
st.sidebar.subheader("Inventario")
precio_bulto = st.sidebar.number_input("Precio Bulto (USDT)", help="Referencia interna")
precio_mayor = st.sidebar.number_input("Precio Mayor (USDT)")
precio_detal = st.sidebar.number_input("Precio Detal (USDT)")

st.sidebar.write("---")
st.sidebar.info("Modo de protección: Activo (USDT Anclado)")
