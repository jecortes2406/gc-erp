import streamlit as st

# Configuración de página: Layout Wide y tema claro
st.set_page_config(layout="wide", page_title="ERP Maestro")

# Estilo profesional: Fondo blanco, texto oscuro, legibilidad máxima
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #333333; }
    [data-testid="stSidebar"] { background-color: #f0f2f6; }
    h1, h2, h3 { color: #1e3a8a; }
    .stMetric { background-color: #f9fafb; padding: 15px; border-radius: 10px; border: 1px solid #e5e7eb; }
    </style>
""", unsafe_allow_html=True)

# Lógica de navegación
menu = st.sidebar.radio("Navegación", ["Panel Principal", "Gestión / Inventario"])

if menu == "Gestión / Inventario":
    from modulo_inventario import mostrar_formulario_inventario
    mostrar_formulario_inventario()
else:
    st.title("Panel Gerencial")
