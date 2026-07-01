import streamlit as st
import pandas as pd

def render_modulo_inventario():
    st.markdown("## 📦 GESTIÓN DE INVENTARIO - MÓDULO ADMINISTRADOR")
    
    # 1. INICIALIZACIÓN SEGURA DE LA BASE DE DATOS EN SESIÓN
    if 'db_inventario' not in st.session_state:
        st.session_state.db_inventario = pd.DataFrame(columns=[
            'Código', 'Producto', 'Margen %', 'Comisión %', 'Precio Venta (Bs)'
        ])
    
    # 2. FORMULARIO DE REGISTRO
    with st.form("registro_maestro_editable", clear_on_submit=True):
        c1, c2 = st.columns(2)
        codigo = c1.text_input("Código SKU")
        producto = c2.text_input("Nombre del Producto")
        
        c3, c4, c5 = st.columns(3)
        costo_usd = c3.number_input("Costo Real (USD)", min_value=0.0, format="%.2f")
        margen_utilidad = c4.number_input("Margen Utilidad (%)", min_value=0.0, format="%.2f")
        comision_vendedor = c5.number_input("Comisión Vendedor (%)", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("💾 REGISTRAR PRODUCTO"):
            # Lógica dinámica usando las tasas que configuraste en el sidebar
            tasa_usada = st.session_state.get('tasa_binance', 46.50)
            
            # Cálculo editable según tu requerimiento
            precio_base = (costo_usd / 0.70) * tasa_usada
            precio_venta = precio_base * (1 + (margen_utilidad / 100))
            
            # Creación del nuevo registro
            nuevo_registro = pd.DataFrame([{
                'Código': codigo, 
                'Producto': producto, 
                'Margen %': margen_utilidad, 
                'Comisión %': comision_vendedor, 
                'Precio Venta (Bs)': precio_venta
            }])
            
            # Concatenación segura
            st.session_state.db_inventario = pd.concat([st.session_state.db_inventario, nuevo_registro], ignore_index=True)
            st.success(f"Producto {producto} registrado con éxito.")

    # 3. VISUALIZACIÓN DE LA MATRIZ (Solo si existe)
    st.subheader("📋 MATRIZ DE PRODUCTOS")
    if not st.session_state.db_inventario.empty:
        st.dataframe(st.session_state.db_inventario, use_container_width=True)
    else:
        st.info("No hay productos registrados aún.")
