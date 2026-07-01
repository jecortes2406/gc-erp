import streamlit as st

# 1. CONFIGURACIÓN
st.set_page_config(page_title="GC Grupo Comercial C.A. - ERP", layout="wide")

# 2. MENÚ
st.sidebar.title("MENÚ DE OPERACIONES")
modulo_seleccionado = st.sidebar.radio("Seleccionar:", 
    ["📊 Dashboard", "🗂️ Gestión / Inventario", "🧾 POS", "🛒 Compras", "📈 Reportes"])

# 3. DISTRIBUCIÓN (Aquí está la clave)
# Quitamos las importaciones de la línea 9 y las ponemos solo donde se necesitan
if modulo_seleccionado == "📊 Dashboard":
    from dashboard import render_dashboard
    render_dashboard()
    
elif modulo_seleccionado == "🗂️ Gestión / Inventario":
    from modulo_inventario import render_modulo_inventario
    render_modulo_inventario()
    
elif modulo_seleccionado == "🧾 POS":
    from modulo_pos import render_modulo_pos
    render_modulo_pos()
    
elif modulo_seleccionado == "🛒 Compras":
    from modulo_contable import render_modulo_contable
    render_modulo_contable()

elif modulo_seleccionado == "📈 Reportes":
    st.info("Módulo en desarrollo")
