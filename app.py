import streamlit as st
from database_manager import init_db

init_db()
st.set_page_config(layout="wide", page_title="ERP Profesional")

# CSS para el look gris corporativo (ni muy claro, ni muy oscuro)
st.markdown("""
    <style>
    .stApp { background-color: #f1f3f4; }
    .stMetric { background-color: white; padding: 15px; border-radius: 8px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

# Tasas de Cambio en Barra Lateral
st.sidebar.title("Configuración")
st.sidebar.subheader("Tasas del día")
bcv = st.sidebar.number_input("Tasa BCV", 36.50)
euro = st.sidebar.number_input("Tasa Euro", 40.20)
binance = st.sidebar.number_input("Tasa Binance", 37.10)

menu = st.sidebar.radio("Navegación", ["Panel Principal", "Gestión / Inventario"])

if menu == "Gestión / Inventario":
    from modulo_inventario import mostrar_formulario_inventario
    mostrar_formulario_inventario()
else:
    st.title("Panel Gerencial")
