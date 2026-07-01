import streamlit as st
import pandas as pd
from datetime import datetime

def render_modulo_inventario():
    # 1. Inicialización Robusta
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            'Fecha', 'Código', 'Producto', 'Categoría', 'Unidad', 
            'Costo USD', 'Margen %', 'Precio Venta USD', 'Precio Venta Bs', 
            'Stock', 'Comision_Pct', 'Comision_Valor_USD'
        ])
    
    tasa_master = st.session_state.get('referencia_master', 765.00) # Usando tu tasa actual
    
    st.markdown("## 📦 GESTIÓN DE INVENTARIO")
    
    # 2. Formulario con todos los campos del Excel
    with st.expander("📝 REGISTRO DETALLADO DE PRODUCTO", expanded=True):
        with st.form("form_inventario_completo", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            sku = c1.text_input("Código SKU")
            nombre = c2.text_input("Nombre del Producto")
            categoria = c3.selectbox("Categoría", ["General", "Electrónica", "Servicios", "Alimentos"])
            
            c4, c5, c6 = st.columns(3)
            costo = c4.number_input("Costo de Compra (USD)", min_value=0.0, format="%.2f")
            margen = c5.number_input("Margen de Utilidad (%)", min_value=0.0, value=30.0)
            stock = c6.number_input("Stock Inicial", min_value=0)
            
            c7, c8 = st.columns(2)
            unidad = c7.selectbox("Unidad de Medida", ["Uni", "Caja", "Litros", "Kilos", "Bultos"])
            comision_pct = c8.number_input("Ganancia Vendedor (%)", min_value=0.0, max_value=100.0, value=2.0)
            
            if st.form_submit_button("🚀 GUARDAR Y CALCULAR"):
                # --- MOTOR DE CÁLCULO BLINDADO ---
                precio_usd = costo * (1 + (margen / 100))
                precio_bs = precio_usd * tasa_master
                valor_comision = precio_usd * (comision_pct / 100)
                
                nuevo = pd.DataFrame([{
                    'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Código': sku, 
                    'Producto': nombre, 'Categoría': categoria, 'Unidad': unidad, 
                    'Costo USD': costo, 'Margen %': margen, 'Precio Venta USD': precio_usd,
                    'Precio Venta Bs': precio_bs, 'Stock': stock, 
                    'Comision_Pct': comision_pct, 'Comision_Valor_USD': valor_comision
                }])
                st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
                st.success(f"Producto {nombre} registrado. Precio sugerido: ${precio_usd:.2f}")

    # 3. Matriz con Alertas visuales
    st.subheader("📋 MATRIZ DE INVENTARIO (BD)")
    if not st.session_state.inventario.empty:
        # Formateo para visualización
        display_df = st.session_state.inventario.copy()
        st.data_editor(display_df, use_container_width=True)
    else:
        st.info("La matriz está vacía.")
