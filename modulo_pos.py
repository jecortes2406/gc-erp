import streamlit as st
import pandas as pd
from database_manager import init_db

def render_modulo_pos():
    st.markdown("## 🧾 PUNTO DE VENTA (POS)")
    df = init_db()
    
    if df.empty:
        st.warning("No hay productos en inventario. Registra productos primero.")
        return

    # Selección de producto
    producto_seleccionado = st.selectbox("Seleccionar Producto", df['Producto'].tolist())
    prod_data = df[df['Producto'] == producto_seleccionado].iloc[0]
    
    st.write(f"Precio Detal: {prod_data['Precio Venta (Bs)']} Bs.")
    
    cantidad = st.number_input("Cantidad a vender", min_value=1, value=1)
    vendedor = st.text_input("Nombre del Vendedor")
    
    if st.button("🛒 PROCESAR VENTA"):
        total_venta = cantidad * prod_data['Precio Venta (Bs)']
        comision = total_venta * (prod_data['Comisión %'] / 100)
        
        # Guardar venta en base de datos de ventas (persistente)
        if 'db_ventas' not in st.session_state:
            st.session_state.db_ventas = pd.DataFrame()
            
        nueva_venta = pd.DataFrame([{
            'Producto': producto_seleccionado,
            'Cantidad': cantidad,
            'Total Bs': total_venta,
            'Comisión': comision,
            'Vendedor': vendedor
        }])
        
        st.session_state.db_ventas = pd.concat([st.session_state.db_ventas, nueva_venta], ignore_index=True)
        st.success(f"Venta registrada. Comisión asignada: {comision:.2f} Bs.")

    # Mostrar historial de ventas
    if 'db_ventas' in st.session_state:
        st.subheader("📋 Historial de Ventas")
        st.dataframe(st.session_state.db_ventas, use_container_width=True)
