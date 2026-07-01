import streamlit as st
import pandas as pd

def render_modulo_inventario():
    st.markdown("## 📦 GESTIÓN DE INVENTARIO - MÓDULO ADMINISTRADOR")
    
    with st.form("registro_maestro_editable", clear_on_submit=True):
        c1, c2 = st.columns(2)
        codigo = c1.text_input("Código SKU")
        producto = c2.text_input("Nombre del Producto")
        
        # Campos totalmente editables - SIN VALORES FIJOS
        c3, c4, c5 = st.columns(3)
        costo_usd = c3.number_input("Costo Real (USD)", format="%.2f")
        margen_utilidad = c4.number_input("Margen Utilidad (%)", min_value=0.0, format="%.2f")
        comision_vendedor = c5.number_input("Comisión Vendedor (%)", min_value=0.0, format="%.2f")
        
        # Logística
        c6, c7 = st.columns(2)
        stock = c6.number_input("Stock Inicial", min_value=0, value=0)
        categoria = c7.selectbox("Categoría", ["Víveres", "Tabacos", "Hogar", "Otros"])

        if st.form_submit_button("💾 REGISTRAR PRODUCTO"):
            # Lógica dinámica: Usa las tasas que el admin puso en el sidebar
            tasa_usada = st.session_state.tasa_binance
            
            # Cálculo editable
            precio_base = (costo_usd / 0.70) * tasa_usada
            precio_venta = precio_base * (1 + (margen_utilidad / 100))
            
            nuevo = pd.DataFrame([{
                'Código': codigo, 'Producto': producto, 'Margen %': margen_utilidad,
                'Comisión %': comision_vendedor, 'Precio Venta (Bs)': precio_venta
            }])
            
            if 'db_inventario' not in st.session_state:
                st.session_state.db_inventario = pd.DataFrame()
            st.session_state.db_inventario = pd.concat([st.session_state.db_inventario, nuevo], ignore_index=True)
            st.success("Producto registrado con los parámetros configurados.")

    st.dataframe(st.session_state.db_inventario, use_container_width=True)
