import streamlit as st
# Importamos la función desde tu archivo (asegúrate que el nombre sea correcto)
from modulo_inventario import mostrar_formulario_inventario

st.set_page_config(layout="wide")

# Barra lateral para navegación
st.sidebar.title("Navegación")
modulo_seleccionado = st.sidebar.radio(
    "Selecciona un módulo:",
    ["Panel Principal / Dashboard", "Gestión / Inventario"]
)

# Lógica de navegación principal (Totalmente plana para evitar errores)
if modulo_seleccionado == "Gestión / Inventario":
    mostrar_formulario_inventario()

elif modulo_seleccionado == "Panel Principal / Dashboard":
    st.title("Dashboard")
    st.write("Bienvenido al panel principal.")
