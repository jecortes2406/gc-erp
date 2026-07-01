import streamlit as st
import pandas as pd
from database_manager import init_db

def render_modulo_inventario():
    # 1. Obtenemos la base de datos centralizada
    df = init_db()
    
    st.markdown("## 📦 GESTIÓN DE INVENTARIO - MÓDULO ADMINISTRADOR")
    
    # 2. Formulario de registro (Editable)
    with st.form("registro_maestro_editable", clear_on_submit=True):
        c1, c2 = st.columns(2)
        codigo = c1.text_input("Código SKU")
        producto = c2.text_input("Nombre del Producto")
        
        c3, c4, c5 = st.columns(3)
        costo_usd = c3.number_input("Costo Real (USD)", min_value=0.0, format="%.2f")
        margen_utilidad = c4.number_input("Margen Utilidad (%)", min_value=0.0, format="%.2f")
        comision_vendedor = c5.number_input("Comisión Vendedor (%)", min_value=0.0, format="%.2f")
        
        categoria = st.selectbox("Categoría", ["Víveres", "Tabacos", "Hogar", "Otros"])

        if st.form_submit_button("💾 REGISTRAR PRODUCTO"):
            # Usamos la tasa que el admin puso en el sidebar del main.py
            tasa_usada = st.session_state.get('tasa_binance', 46.50)
            
            # Cálculo de precios según tu lógica editable
            precio_base = (costo_usd / 0.70) * tasa_usada
            precio_venta = precio_base * (1 + (margen_utilidad / 100))
            
            # Nuevo registro
            nuevo = pd.DataFrame([{
                'Código': codigo, 
                'Producto': producto, 
                'Categoría': categoria,
                'Costo USD': costo_usd,
                'Margen %': margen_utilidad, 
                'Comisión %': comision_vendedor, 
                'Precio Venta (Bs)': precio_venta
            }])
            
            # Guardamos en la base de datos centralizada
            st.session_state.db_inventario = pd.concat([st.session_state.db_inventario, nuevo], ignore_index=True)
            st.success(f"Producto {producto} registrado con éxito.")

    # 3. Visualización de la Matriz (Ahora lee de forma segura)
    st.subheader("📋 MATRIZ DE PRODUCTOS")
    if not st.session_state.db_inventario.empty:
        st.dataframe(st.session_state.db_inventario, use_container_width=True)
    else:
        st.info("No hay productos registrados aún.")
