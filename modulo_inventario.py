import streamlit as st
import pandas as pd
from datetime import datetime

def render_modulo_inventario():
    # Recuperamos la Tasa Maestra que definiste en tu app.py
    tasa_master = st.session_state.get('referencia_master', 46.50)
    
    st.markdown("## 📦 GESTIÓN DE INVENTARIO")
    
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            'Fecha', 'Código', 'Producto', 'Categoría', 'Unidad', 
            'Costo USD', 'Margen %', 'Precio Venta Bs', 'Stock'
        ])

    # Formulario
    st.markdown('<div class="card-white">', unsafe_allow_html=True)
    st.subheader("📝 REGISTRO DETALLADO")
    with st.form("form_inventario_completo", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        sku = c1.text_input("Código SKU")
        nombre = c2.text_input("Nombre del Producto")
        categoria = c3.selectbox("Categoría", ["General", "Electrónica", "Servicios", "Alimentos"])
        
        c4, c5, c6, c7 = st.columns(4)
        costo_usd = c4.number_input("Costo USD", min_value=0.0, format="%.2f")
        margen = c5.number_input("Margen %", min_value=0.0, value=30.0)
        stock = c6.number_input("Stock Inicial", min_value=0)
        unidad = c7.selectbox("Unidad", ["Uni", "Caja", "Kilo", "Bulto"])
        
        if st.form_submit_button("🚀 GUARDAR PRODUCTO", type="primary"):
            precio_bs = (costo_usd * (1 + (margen/100))) * tasa_master
            nuevo = pd.DataFrame([{
                'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Código': sku, 
                'Producto': nombre, 'Categoría': categoria, 'Unidad': unidad, 
                'Costo USD': costo_usd, 'Margen %': margen, 
                'Precio Venta Bs': precio_bs, 'Stock': stock
            }])
            st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
            st.success("Guardado.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Matriz
    st.subheader("📋 MATRIZ DE INVENTARIO")
    st.data_editor(st.session_state.inventario, use_container_width=True)
