import streamlit as st
from database_manager import init_db

# 1. Configuración y carga de DB
st.set_page_config(page_title="GC Grupo Comercial C.A. - ERP", layout="wide")
init_db() 

# 2. Navegación
st.sidebar.title("MENÚ PRINCIPAL")
modulo = st.sidebar.radio("Seleccionar:", ["📊 Dashboard", "🗂️ Inventario", "🧾 POS", "🛒 Compras"])

# 3. Distribución con manejo de errores
if modulo == "📊 Dashboard":
    from dashboard import render_dashboard
    render_dashboard()
elif modulo == "🗂️ Inventario":
    from modulo_inventario import render_modulo_inventario
    render_modulo_inventario()
elif modulo == "🧾 POS":
    from modulo_pos import render_modulo_pos
    render_modulo_pos()
elif modulo == "🛒 Compras":
    from modulo_contable import render_modulo_contable
    render_modulo_contable()
