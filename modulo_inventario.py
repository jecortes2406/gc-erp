import streamlit as st

def mostrar_formulario_inventario():
    st.markdown("## 🏢 GESTIÓN DE INVENTARIO MAESTRO")
    
    # Dashboard inicial (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Valor Venta", "$432.00")
    col2.metric("Stock Bajo", "0")
    col3.metric("Unidades", "840")
    col4.metric("Inversión", "$345.60")
    
    st.markdown("---")
    
    # Formulario con etiquetas y estructura organizada
    with st.form("form_pro"):
        st.subheader("📝 Carga Maestra de Producto")
        
        c1, c2, c3 = st.columns(3)
        c1.text_input("Código SKU")
        c2.text_input("Nombre del Producto")
        c3.date_input("Fecha Vencimiento")
        
        c4, c5 = st.columns(2)
        c4.text_input("Proveedor")
        c5.number_input("Stock Inicial", min_value=0)
        
        st.subheader("💰 Estructura de Costos")
        c6, c7, c8 = st.columns(3)
        c6.number_input("Costo Base ($)", format="%.2f")
        c7.selectbox("Moneda de Pago", ["USDT", "USD", "EUR", "VES"])
        c8.number_input("Stock Mínimo (Alerta)")
        
        st.subheader("📊 Escala de Precios y Ventas")
        c9, c10, c11 = st.columns(3)
        c9.number_input("Margen Detal (%)")
        c10.number_input("Margen Bulto (%)")
        c11.number_input("Margen Mayor (%)")
        
        c12, c13 = st.columns(2)
        c12.selectbox("IVA", ["Sin IVA", "Con IVA"])
        c13.text_input("Vendedor")
        
        st.file_uploader("Subir Imagen Catálogo")
        
        if st.form_submit_button("GUARDAR PRODUCTO"):
            st.success("Producto registrado correctamente.")
