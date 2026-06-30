import streamlit as st

def mostrar_formulario_inventario():
    if 'modo_ingreso' not in st.session_state: st.session_state.modo_ingreso = False

    if not st.session_state.modo_ingreso:
        st.markdown("## 🏢 INVENTARIO MAESTRO")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Valor Venta", "$432.00"); col2.metric("Stock Bajo", "0")
        col3.metric("Unidades", "840"); col4.metric("Inversión", "$345.60")
        
        if st.button("＋ NUEVO PRODUCTO"):
            st.session_state.modo_ingreso = True
            st.rerun()
    else:
        with st.form("carga_pro"):
            st.subheader("1. Datos Básicos")
            c1, c2, c3 = st.columns(3)
            sku = c1.text_input("SKU"); nombre = c2.text_input("Nombre"); venc = c3.date_input("Vencimiento")
            c4, c5 = st.columns(2)
            prov = c4.text_input("Proveedor"); stock = c5.number_input("Stock", 0)
            
            st.subheader("2. Costos y Fiscalidad")
            c6, c7, c8 = st.columns(3)
            costo = c6.number_input("Costo $", format="%.2f"); mon = c7.selectbox("Moneda", ["USDT", "USD", "EUR"]); min_stk = c8.number_input("Stock Mínimo", 0)
            
            st.subheader("3. Márgenes y Ventas")
            c9, c10, c11 = st.columns(3)
            m_det = c9.number_input("Margen Detal %"); m_bul = c10.number_input("Margen Bulto %"); m_may = c11.number_input("Margen Mayor %")
            c12, c13 = st.columns(2)
            iva = c12.selectbox("IVA", ["Sin IVA", "Con IVA"]); vend = c13.text_input("Vendedor"); com = c13.number_input("Comisión %")
            img = st.file_uploader("Imagen Catálogo", type=['jpg', 'png'])
            
            if st.form_submit_button("GUARDAR"):
                st.session_state.modo_ingreso = False
                st.rerun()
        if st.button("VOLVER"):
            st.session_state.modo_ingreso = False
            st.rerun()
