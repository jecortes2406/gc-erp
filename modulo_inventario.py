import streamlit as st
import pandas as pd

def render_modulo_inventario():
    st.markdown("## 📦 GESTIÓN DE INVENTARIO - MÓDULO MAESTRO")
    
    # 1. Definición de la Matriz Maestra con todas las columnas
    columnas = [
        'Código', 'Producto', 'Categoría', 'Vencimiento', 'Cant x Bulto', 
        'Stock', 'Alerta', 'Costo', 'Moneda', 'Precio Detal', 
        'Precio Bulto', 'Precio Mayor'
    ]
    
    if 'df_inventario' not in st.session_state:
        st.session_state.df_inventario = pd.DataFrame(columns=columnas)
    
    # 2. Formulario de Registro con todos los campos
    with st.form("registro_maestro", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        codigo = c1.text_input("Código")
        producto = c2.text_input("Producto")
        categoria = c3.selectbox("Categoría", ["Víveres", "Tabacos", "Hogar", "Otros"])
        
        c4, c5, c6 = st.columns(3)
        vencimiento = c4.date_input("Fecha Vencimiento")
        cant_bulto = c5.number_input("Cant x Bulto", value=1)
        stock = c6.number_input("Stock", value=0)
        
        c7, c8, c9 = st.columns(3)
        costo = c7.number_input("Costo", format="%.2f")
        moneda = c8.selectbox("Moneda", ["BS", "EU", "USDT"])
        margen = c9.number_input("Margen (%)", value=30.0)
        
        if st.form_submit_button("💾 REGISTRAR PRODUCTO"):
            # Lógica de precios
            p_detal = costo * (1 + (margen/100))
            alerta = "⚠️ STOP BAJO" if stock < 5 else "✅ OK"
            
            nuevo = pd.DataFrame([{
                'Código': codigo, 'Producto': producto, 'Categoría': categoria,
                'Vencimiento': vencimiento, 'Cant x Bulto': cant_bulto, 'Stock': stock,
                'Alerta': alerta, 'Costo': costo, 'Moneda': moneda,
                'Precio Detal': p_detal, 'Precio Bulto': p_detal*0.9, 
                'Precio Mayor': p_detal*0.85
            }])
            
            st.session_state.df_inventario = pd.concat([st.session_state.df_inventario, nuevo], ignore_index=True)
            st.success("Producto registrado con éxito.")

    # 3. Visualización de la Matriz Completa
    st.subheader("📋 MATRIZ DE INVENTARIO (ESPEJO EXCEL)")
    st.dataframe(st.session_state.df_inventario, use_container_width=True)
    
    # Próximo paso: incluir botones de acción (Editar/Borrar) en cada fila
