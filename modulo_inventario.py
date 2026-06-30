import streamlit as st

def mostrar_formulario_inventario():
    st.title("🏢 GESTIÓN DE INVENTARIO MAESTRO")
    
    # Métricas Dashboard
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Valor Venta", "$432.00"); c2.metric("Stock Bajo", "0")
    c3.metric("Unidades", "840"); c4.metric("Inversión", "$345.60")
    
    st.markdown("---")
    
    # Contenedor estilo tarjeta blanca
    with st.container():
        st.subheader("📝 Carga de Producto")
        
        # Identidad
        cols1 = st.columns([2, 2, 1])
        sku = cols1[0].text_input("Código SKU")
        nom = cols1[1].text_input("Nombre del Producto")
        venc = cols1[2].date_input("Vencimiento")
        
        # Estructura de Costos
        st.subheader("💰 Estructura de Costos")
        cols2 = st.columns(3)
        costo = cols2[0].number_input("Costo Base ($)")
        moneda = cols2[1].selectbox("Moneda", ["USDT", "Bolívares", "Euros"])
        comision = cols2[2].number_input("Comisión (%)")
        
        # Márgenes
        st.subheader("📊 Niveles de Venta (Márgenes)")
        cols3 = st.columns(3)
        md = cols3[0].number_input("Margen Detal (%)")
        mb = cols3[1].number_input("Margen Bulto (%)")
        mm = cols3[2].number_input("Margen Mayor (%)")
        
        if st.button("🚀 GUARDAR PRODUCTO", type="primary"):
            st.success("Producto registrado en la base de datos.")
