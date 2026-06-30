import streamlit as st

# Configuración inicial de la página
st.set_page_config(layout="wide", page_title="ERP Maestro")

# Estilo corporativo (fondo gris claro y barra lateral oscura)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# Menú de navegación
menu = st.sidebar.radio("Navegación", ["Panel Principal", "Gestión / Inventario"])

# Lógica de carga de módulos (Evita errores de indentación)
if menu == "Gestión / Inventario":
    from modulo_inventario import mostrar_formulario_inventario
    mostrar_formulario_inventario()
else:
    st.title("Panel Gerencial")
    st.write("Bienvenido al sistema. Selecciona una opción en el menú lateral.")
