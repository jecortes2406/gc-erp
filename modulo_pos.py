import streamlit as st
from database_manager import init_db, save_data

def render_modulo_pos():
    st.markdown("## 🧾 PUNTO DE VENTA (POS)")
    
    # 1. Cargar datos
    init_db()
    
    # 2. Validar que existan datos antes de operar
    if 'db_inventario' in st.session_state and not st.session_state.db_inventario.empty:
        # Aquí va la lógica de ventas
        producto = st.selectbox("Seleccionar Producto", st.session_state.db_inventario['Producto'])
        # ... lógica de venta ...
    else:
        st.warning("⚠️ El inventario está vacío. Registra productos primero.")
