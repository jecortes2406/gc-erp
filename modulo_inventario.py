import streamlit as st
import pandas as pd

def render_modulo_inventario():
    st.markdown("## 🗂️ GESTIÓN DE INVENTARIO - REPLICA EXCEL")
    
    # 1. DEFINICIÓN DE ESTRUCTURA (Columnas de tu Excel)
    columnas = [
        'Código', 'Producto', 'Vencimiento', 'Cant x Bulto', 'Stock', 
        'Costo', 'Margen %', 'Precio Detal', 'Precio Bulto', 'Alerta'
    ]
    
    # Inicialización de la tabla con tus columnas
    if 'inventario_total' not in st.session_state:
        st.session_state.inventario_total = pd.DataFrame(columns=columnas)
    
    # 2. FORMULARIO DE ENTRADA (Captura todos los campos)
    with st.form("form_replicar_excel"):
        c1, c2, c3 = st.columns(3)
        codigo = c1.text_input("Código")
        producto = c2.text_input("Producto")
        vencimiento = c3.date_input("Fecha Vencimiento")
        
        c4, c5, c6 = st.columns(3)
        bulto = c4.number_input("Cantidad x Bulto", value=1)
        stock = c5.number_input("Stock", value=0)
        costo = c6.number_input("Costo", format="%.2f")
        
        margen = st.number_input("Margen (%)", value=30.0)
        
        if st.form_submit_button("💾 REGISTRAR PRODUCTO"):
            # Lógica de cálculo replicando tu Excel
            p_detal = costo * (1 + (margen/100))
            p_bulto = p_detal * 0.9 # Ejemplo: 10% descuento por bulto
            alerta = "⚠️ BAJO" if stock < 5 else "✅ OK"
            
            nuevo = pd.DataFrame([{
                'Código': codigo, 'Producto': producto, 'Vencimiento': vencimiento,
                'Cant x Bulto': bulto, 'Stock': stock, 'Costo': costo,
                'Margen %': margen, 'Precio Detal': p_detal, 
                'Precio Bulto': p_bulto, 'Alerta': alerta
            }])
            
            st.session_state.inventario_total = pd.concat([st.session_state.inventario_total, nuevo], ignore_index=True)
            st.rerun()

    # 3. VISUALIZACIÓN DE LA MATRIZ (Aquí verás TODO tu Excel)
    st.subheader("📋 MATRIZ DE INVENTARIO COMPLETA")
    st.dataframe(st.session_state.inventario_total, use_container_width=True)
