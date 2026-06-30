import streamlit as st

def mostrar_formulario_inventario():
    # Estilo CSS para forzar cajas blancas y diseño limpio
    st.markdown("""
        <style>
        .stApp { background-color: #f0f2f6; }
        input, select, textarea { background-color: white !important; color: black !important; border: 1px solid #ccc !important; }
        .stForm { background-color: white; padding: 20px; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.header("🏢 Gestión de Inventario")

    # Métrica superior profesional
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Valor Venta", "$432.00")
    c2.metric("Stock Bajo", "0")
    c3.metric("Unidades", "840")
    c4.metric("Inversión", "$345.60")

    st.markdown("---")

    # Formulario con columnas forzadas
    with st.form("form_limpio"):
        st.subheader("📝 Datos del Producto")
        
        # Fila 1
        col1, col2, col3 = st.columns(3)
        sku = col1.text_input("Código SKU")
        nombre = col2.text_input("Nombre del Producto")
        venc = col3.date_input("Vencimiento")
        
        # Fila 2
        col4, col5 = st.columns(2)
        prov = col4.text_input("Proveedor")
        stock = col5.number_input("Stock Inicial", min_value=0)
        
        st.subheader("💰 Estructura de Precios")
        # Fila 3
        col6, col7, col8 = st.columns(3)
        costo = col6.number_input("Costo Base ($)")
        mon = col7.selectbox("Moneda", ["USDT", "USD", "EUR"])
        iva = col8.selectbox("Estatus IVA", ["Sin IVA", "Con IVA"])
        
        # Fila 4
        col9, col10, col11 = st.columns(3)
        m_det = col9.number_input("Margen Detal (%)")
        m_bul = col10.number_input("Margen Bulto (%)")
        m_may = col11.number_input("Margen Mayor (%)")
        
        # Acción final
        btn = st.form_submit_button("🚀 GUARDAR PRODUCTO")
        if btn:
            st.success("Guardado correctamente.")
