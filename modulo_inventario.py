import streamlit as st

def mostrar_formulario_inventario():
    # Tarjetas de Métricas (Dashboard Superior)
    st.markdown("## 🏢 INVENTARIO MAESTRO")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Valor Venta Total", "$432.00", "+5%")
    col2.metric("Stock Bajo", "0", delta_color="inverse")
    col3.metric("Unidades en Almacén", "840")
    col4.metric("Inversión en Stock", "$345.60")

    st.markdown("---")
    
    # Botón de acción con estilo
    if st.button("＋ AGREGAR PRODUCTO", type="primary"):
        st.session_state.modo_ingreso = True
        st.rerun()
    
    # Aquí irá tu rejilla (grid) de productos
    st.write("Tabla de inventario profesional próximamente...")
