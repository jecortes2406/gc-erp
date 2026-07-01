import streamlit as st
import pandas as pd
from datetime import datetime

def render_modulo_inventario():
    # Inicialización del estado de inventario (Memoria temporal robusta)
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            'Fecha', 'Código', 'Producto', 'Categoría', 'Unidad', 
            'Costo USD', 'Margen %', 'Stock', 'Comision_Pct', 'Precio Venta Bs'
        ])
    
    tasa_master = st.session_state.get('referencia_master', 46.50)
    
    st.markdown("## 📦 GESTIÓN DE INVENTARIO")
    
    # Bloque de Registro
    with st.container():
        st.subheader("📝 NUEVO PRODUCTO (Blindado)")
        with st.form("form_inventario", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            sku = col1.text_input("Código SKU")
            nombre = col2.text_input("Nombre del Producto")
            categoria = col3.selectbox("Categoría", ["General", "Electrónica", "Servicios", "Alimentos"])
            
            col4, col5, col6, col7 = st.columns(4)
            costo_usd = col4.number_input("Costo USD", min_value=0.0, format="%.2f")
            margen = col5.number_input("Margen %", value=30.0)
            stock = col6.number_input("Stock Inicial", min_value=0)
            unidad = col7.selectbox("Unidad", ["Uni", "Caja", "Kilo", "Bulto"])
            
            comision = st.number_input("Comisión Vendedor (%)", min_value=0.0, max_value=100.0, value=5.0)
            
            if st.form_submit_button("🚀 GUARDAR Y BLINDAR"):
                precio_venta = (costo_usd * (1 + (margen/100))) * tasa_master
                nuevo_reg = pd.DataFrame([{
                    'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Código': sku, 
                    'Producto': nombre, 'Categoría': categoria, 'Unidad': unidad, 
                    'Costo USD': costo_usd, 'Margen %': margen, 'Stock': stock, 
                    'Comision_Pct': comision, 'Precio Venta Bs': precio_venta
                }])
                st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo_reg], ignore_index=True)
                st.success("Producto registrado exitosamente.")

    # Matriz de Visualización
    st.subheader("📋 MATRIZ DE INVENTARIO (BD)")
    st.data_editor(st.session_state.inventario, use_container_width=True)
