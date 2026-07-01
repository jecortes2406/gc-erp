import streamlit as st
import pandas as pd
from datetime import datetime
# Importamos las funciones de tu base de datos sin tocar nada anterior
from database_manager import insertar_producto, obtener_todos_productos

def render_modulo_inventario():
    # Recuperamos la Tasa Maestra que definiste en tu app.py
    tasa_master = st.session_state.get('referencia_master', 46.50)
    
    st.markdown("## 📦 GESTIÓN DE INVENTARIO")
    
    # Formulario
    st.markdown('<div class="card-white">', unsafe_allow_html=True)
    st.subheader("📝 REGISTRO DETALLADO")
    
    with st.form("form_inventario_completo", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        sku = c1.text_input("Código SKU")
        nombre = c2.text_input("Nombre del Producto")
        categoria = c3.selectbox("Categoría", ["General", "Electrónica", "Servicios", "Alimentos"])
        
        c4, c5, c6, c7 = st.columns(4)
        costo_usd = c4.number_input("Costo USD", min_value=0.0, format="%.2f")
        margen = c5.number_input("Margen %", min_value=0.0, value=30.0)
        stock = c6.number_input("Stock Inicial", min_value=0)
        unidad = c7.selectbox("Unidad", ["Uni", "Caja", "Kilo", "Bulto"])
        
        if st.form_submit_button("🚀 GUARDAR PRODUCTO", type="primary"):
            # Lógica de cálculo que ya tenías
            precio_bs = (costo_usd * (1 + (margen/100))) * tasa_master
            
            # ANEXO: Guardar en la base de datos real (no solo en memoria)
            # Adaptamos tus campos a la tabla que creamos
            insertar_producto(nombre, sku, costo_usd, precio_bs/tasa_master, precio_bs, stock)
            
            st.success(f"Producto {nombre} guardado en base de datos.")
            
    st.markdown('</div>', unsafe_allow_html=True)

    # MATRIZ DINÁMICA (ANEXO)
    st.subheader("📋 MATRIZ DE INVENTARIO (BD)")
    
    # Recuperamos los datos de la base de datos en lugar de solo el session_state
    data = obtener_todos_productos()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Nombre", "SKU", "Costo", "Precio_Base", "Precio_Venta_Bs", "Stock"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no hay productos registrados en la base de datos.")
