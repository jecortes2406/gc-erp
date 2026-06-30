import streamlit as st

def mostrar_formulario_inventario():
    st.title("Gestión de Inventario")
    
    # Usamos st.session_state para controlar la vista sin errores
    if 'vista_inventario' not in st.session_state:
        st.session_state.vista_inventario = 'listado'

    if st.session_state.vista_inventario == 'listado':
        if st.button("＋ Agregar Nuevo Producto"):
            st.session_state.vista_inventario = 'formulario'
            st.rerun()
        st.write("Aquí irá la tabla de productos.")
        
    elif st.session_state.vista_inventario == 'formulario':
        with st.form("nuevo_producto"):
            st.subheader("Datos del Producto")
            sku = st.text_input("Código SKU:")
            nombre = st.text_input("Nombre del Producto:")
            costo = st.number_input("Costo Base:", min_value=0.0)
            
            if st.form_submit_button("Guardar"):
                st.success("Producto guardado.")
                st.session_state.vista_inventario = 'listado'
                st.rerun()
        
        if st.button("Volver"):
            st.session_state.vista_inventario = 'listado'
            st.rerun()
