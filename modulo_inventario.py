import streamlit as st
import pandas as pd
from datetime import datetime

def render_modulo_inventario():
    # Usamos la referencia maestra de tu app.py si existe, sino, valor por defecto
    tasa_master = st.session_state.get('referencia_master', 46.50)
    
    st.markdown("## 📦 GESTIÓN DE INVENTARIO")
    
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            'Fecha', 'Código', 'Producto', 'Costo USD', 'Tasa Ref', 'Precio Venta Bs'
        ])

    st.markdown('<div class="card-white">', unsafe_allow_html=True)
    st.subheader("📝 NUEVO PRODUCTO (Blindado)")
    
    with st.form("form_inventario_pro", clear_on_submit=True):
        c1, c2 = st.columns(2)
        sku = c1.text_input("Código SKU")
        nombre = c2.text_input("Nombre del Producto")
        
        c3, c4 = st.columns(2)
        costo_usd = c3.number_input("Costo (USD)", min_value=0.0, format="%.2f")
        margen = c4.number_input("Margen de Ganancia (%)", min_value=0.0, value=30.0)
        
        if st.form_submit_button("🚀 GUARDAR Y BLINDAR", type="primary"):
            precio_bs = (costo_usd * (1 + (margen/100))) * tasa_master
            nuevo = pd.DataFrame([{
                'Fecha': datetime.now().strftime("%Y-%m-%d"),
                'Código': sku, 'Producto': nombre, 'Costo USD': costo_usd,
                'Tasa Ref': tasa_master, 'Precio Venta Bs': precio_bs
            }])
            st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
            st.success(f"Producto registrado. Precio proyectado: Bs. {precio_bs:,.2f}")
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("📋 Inventario Actual")
    st.data_editor(st.session_state.inventario, use_container_width=True)
