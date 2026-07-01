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
    
    # Recuperamos la tasa desde el session_state (definida en app.py)
    tasa_master = st.session_state.get('referencia_master', 46.50)
    
    st.markdown("## 📦 GESTIÓN DE INVENTARIO")
    
    # 2. Formulario de Registro
    with st.expander("📝 REGISTRO DETALLADO DE PRODUCTO", expanded=True):
        with st.form("form_inventario_completo", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            sku = c1.text_input("Código SKU")
            nombre = c2.text_input("Nombre del Producto")
            # Corrección de sintaxis en la lista de categorías
            categorias = ["General", "Electrónica", "Tabacos", "Heladería", "Bebidas", "Confitería", "Hogar", "Especias", "Servicios", "Víveres"]
            categoria = c3.selectbox("Categoría", categorias)
            
            c4, c5, c6 = st.columns(3)
            costo = c4.number_input("Costo de Compra (USD)", min_value=0.0, format="%.2f")
            margen = c5.number_input("Margen de Utilidad (%)", min_value=0.0, value=30.0)
            stock = c6.number_input("Stock Inicial", min_value=0)
            
            c7, c8 = st.columns(2)
            unidad = c7.selectbox("Unidad de Medida", ["Uni", "Caja", "Litros", "Kilos", "Bultos"])
            comision_pct = c8.number_input("Ganancia Vendedor (%)", min_value=0.0, max_value=100.0, value=2.0)
            
            if st.form_submit_button("🚀 GUARDAR Y CALCULAR"):
                # --- MOTOR DE CÁLCULO BLINDADO ---
                # Precio = Costo + Margen
                precio_usd = costo * (1 + (margen / 100))
                # Conversión a Bs usando la tasa maestra del sistema
                precio_bs = precio_usd * tasa_master
                # Comisión calculada sobre el precio final de venta
                valor_comision = precio_usd * (comision_pct / 100)
                
                nuevo = pd.DataFrame([{
                    'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Código': sku, 
                    'Producto': nombre, 'Categoría': categoria, 'Unidad': unidad, 
                    'Costo USD': costo, 'Margen %': margen, 'Precio Venta USD': precio_usd,
                    'Precio Venta Bs': precio_bs, 'Stock': stock, 
                    'Comision_Pct': comision_pct, 'Comision_Valor_USD': valor_comision
                }])
                
                st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
                st.success(f"Producto {nombre} registrado correctamente.")

    # 3. Matriz de Inventario
    st.subheader("📋 MATRIZ DE INVENTARIO (BD)")
    if not st.session_state.inventario.empty:
        st.data_editor(st.session_state.inventario, use_container_width=True)
    else:
        st.info("La matriz está vacía. Registra tu primer producto.")
