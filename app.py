# --- NAVEGACIÓN PRINCIPAL (app.py) ---
# Asegúrate de que esto esté al nivel correcto de indentación
if modulo_seleccionado == "Gestión / Inventario":
    # Llamamos a tu módulo de inventario
    from modulo_inventario import mostrar_formulario_inventario
    mostrar_formulario_inventario()

elif modulo_seleccionado == "Panel Principal / Dashboard":
    st.title("Panel Principal")
    # Aquí irá tu lógica de Dashboard
