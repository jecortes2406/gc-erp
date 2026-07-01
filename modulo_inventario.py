import streamlit as st
import pandas as pd

def render_modulo_inventario():
    # 1. Definición del Esquema Maestro
    columnas = [
        'Código', 'Producto', 'Categoría', 'Vencimiento', 'Cant x Bulto', 
        'Stock', 'Proveedor', 'Costo USD', 'Tasa Uso', 'Moneda', 
        'Utilidad %', 'Precio Detal', 'Precio Mayor', 'Precio Bulto'
    ]
    
    # 2. Inicialización de la "Base de Datos" en memoria
    if 'df_maestro' not in st.session_state:
        st.session_state.df_maestro = pd.DataFrame(columns=columnas)
        
    st.markdown("## 📦 GESTIÓN DE INVENTARIO - SISTEMA MAESTRO")
    
    # 3. Formulario estructurado según tus necesidades
    with st.form("form_registro_limpio", clear_on_submit=True):
        st.subheader("📝 1. Identidad y Logística")
        c1, c2, c3 = st.columns(3)
        nombre = c1.text_input("Nombre Comercial")
        codigo = c2.text_input("Código SKU")
        cat = c3.selectbox("Categoría", ["Víveres", "Tabacos", "Hogar"])
        
        c4, c5, c6 = st.columns(3)
        vencimiento = c4.date_input("Fecha Vencimiento")
        stock = c5.number_input("Stock Inicial", value=0)
        proveedor = c6.text_input("Proveedor")
        
        st.subheader("💰 2. Datos de Inversión y Precios")
        c7, c8, c9 = st.columns(3)
        costo = c7.number_input("Costo USD", format="%.2f")
        tasa = c8.number_input("Tasa Aplicada", value=st.session_state.get('tasa_binance', 46.50))
        moneda = c9.selectbox("Moneda Pago", ["BS", "EU", "USDT"])
        
        utilidad = st.number_input("Utilidad Aspirada (%)", value=30.0)
        
        if st.form_submit_button("💾 GUARDAR PRODUCTO MAESTRO"):
            # Lógica de cálculo (Anclaje a tasa manual)
            precio_base_bs = (costo / 0.70) * tasa
            precio_final = precio_base_bs * (1 + (utilidad/100))
            
            nuevo_prod = pd.DataFrame([{
                'Código': codigo, 'Producto': nombre, 'Categoría': cat,
                'Vencimiento': vencimiento, 'Stock': stock, 'Proveedor': proveedor,
                'Costo USD': costo, 'Tasa Uso': tasa, 'Moneda': moneda,
                'Utilidad %': utilidad, 'Precio Detal': precio_final,
                'Precio Mayor': precio_final * 0.95, 'Precio Bulto': precio_final * 0.90
            }])
            
            st.session_state.df_maestro = pd.concat([st.session_state.df_maestro, nuevo_prod], ignore_index=True)
            st.rerun()

    # 4. Matriz de Destino (Aquí cae el producto al guardar)
    st.subheader("📋 MATRIZ DE PRODUCTOS")
    st.dataframe(st.session_state.df_maestro, use_container_width=True)
