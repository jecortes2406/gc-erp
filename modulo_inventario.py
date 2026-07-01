import streamlit as st
import pandas as pd
from datetime import datetime

def render_modulo_inventario():
    st.title("🛡️ Gestión de Inventario con Registro Cambiario")

    # Inicialización de estado
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame(columns=[
            'Fecha Registro', 'Código', 'Producto', 'Costo USD', 
            'Tasa BCV', 'Tasa Binance', 'Precio Venta Bs', 'Margen %'
        ])

    # --- 1. Formulario de Incorporación con Registro de Tasas ---
    with st.expander("➕ Incorporar Producto (Registro de Tasas)", expanded=True):
        with st.form("form_blindado_completo", clear_on_submit=True):
            col1, col2 = st.columns(2)
            codigo = col1.text_input("Código de Producto")
            producto = col2.text_input("Nombre del Producto")
            
            c3, c4, c5 = st.columns(3)
            costo_usd = c3.number_input("Costo de Compra (USD)", min_value=0.0, format="%.2f")
            tasa_bcv = c4.number_input("Tasa BCV al momento", value=35.0, format="%.2f")
            tasa_binance = c5.number_input("Tasa Binance al momento", value=36.5, format="%.2f")
            
            margen = st.number_input("Margen de Ganancia (%)", min_value=0.0, value=30.0)
            
            submit = st.form_submit_button("Registrar y Blindar Producto")
            
            if submit:
                # Cálculo utilizando la tasa de Binance como referencia de mercado para blindaje
                precio_venta_bs = (costo_usd * (1 + (margen/100))) * tasa_binance
                
                nuevo_prod = pd.DataFrame([{
                    'Fecha Registro': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'Código': codigo, 'Producto': producto, 'Costo USD': costo_usd,
                    'Tasa BCV': tasa_bcv, 'Tasa Binance': tasa_binance,
                    'Precio Venta Bs': precio_venta_bs, 'Margen %': margen
                }])
                st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo_prod], ignore_index=True)
                st.success("Producto registrado con tasas de referencia guardadas.")

    # --- 2. Tabla de Gestión y Exportación ---
    st.subheader("Inventario con Registro de Tasas")
    
    if not st.session_state.inventario.empty:
        # Botón de exportación a Excel
        csv = st.session_state.inventario.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Inventario a Excel (CSV)",
            data=csv,
            file_name='inventario_blindado.csv',
            mime='text/csv'
        )
        
        st.data_editor(st.session_state.inventario, use_container_width=True)

if _name_ == "_main_":
    render_modulo_inventario()
