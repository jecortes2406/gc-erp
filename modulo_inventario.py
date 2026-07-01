import streamlit as st
import pandas as pd

def render_modulo_inventario():
    st.markdown("## 📦 GESTIÓN DE INVENTARIO - SISTEMA MAESTRO")
    
    # Creamos pestañas para separar la acción de la visualización
    tab1, tab2 = st.tabs(["➕ NUEVO PRODUCTO", "📋 MATRIZ DE INVENTARIO"])
    
    with tab1:
        with st.form("form_nuevo_producto", clear_on_submit=True):
            # SECCIÓN 1: ESPECIFICACIONES DE IDENTIDAD
            st.subheader("📝 Especificaciones de Identidad")
            c1, c2 = st.columns(2)
            nombre = c1.text_input("Nombre Comercial")
            categoria = c2.selectbox("Categoría / Pasillo", ["Víveres", "Tabacos", "Hogar", "Otros"])
            
            c3, c4 = st.columns(2)
            codigo = c3.text_input("Código SKU")
            marca = c4.text_input("Marca / Fabricante")
            
            # SECCIÓN 2: LOGÍSTICA DE ALMACENAJE
            st.subheader("📦 Logística de Almacenaje")
            l1, l2, l3 = st.columns(3)
            sede = l1.text_input("Centro de Recepción")
            unidad = l2.selectbox("Unidad de Gestión", ["Uni", "Caja", "Kilos", "Litros"])
            stock_min = l3.number_input("Stock Mínimo Crítico", value=5)
            
            # SECCIÓN 3: ESTRUCTURA DE PRECIOS
            st.subheader("💰 Estructura de Precios")
            p1, p2, p3 = st.columns(3)
            p1.number_input("Precio al Detal (USD)", format="%.2f")
            p2.number_input("Precio al Mayor (USD)", format="%.2f")
            p3.number_input("Precio por Bulto (USD)", format="%.2f")
            
            if st.form_submit_button("🚀 GUARDAR PRODUCTO MAESTRO"):
                # Aquí iría la lógica para guardar en tu CSV (archivo master)
                st.success(f"Producto {nombre} guardado correctamente.")
    
    with tab2:
        st.subheader("📋 Matriz de Inventario")
        # Aquí cargaremos el archivo CSV que venimos trabajando
        if 'df_inventario' in st.session_state and not st.session_state.df_inventario.empty:
            st.dataframe(st.session_state.df_inventario, use_container_width=True)
        else:
            st.info("La matriz está limpia. Registra tu primer producto en la pestaña 'NUEVO PRODUCTO'.")
