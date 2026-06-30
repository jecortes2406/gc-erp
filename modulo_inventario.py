import streamlit as st

def mostrar_formulario_inventario():
    # Estilo profesional: fondo limpio y contenedores con borde
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa; }
        .css-1r6slb0 { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        </style>
    """, unsafe_allow_html=True)

    st.header("🏢 Gestión de Inventario")

    # --- DASHBOARD DE MÉTRICAS (Igual a tu foto) ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Valor Venta Total", "$432.00")
    m2.metric("Stock Bajo", "0")
    m3.metric("Unidades", "840")
    m4.metric("Inversión", "$345.60")

    st.markdown("---")

    # --- FORMULARIO CON DISEÑO PROFESIONAL ---
    # Usamos st.container para crear el bloque de "NUEVO PRODUCTO"
    with st.container():
        st.subheader("📝 Nuevo Producto")
        
        # Bloque de Identidad (Columnas de diferente tamaño)
        c1, c2, c3 = st.columns([2, 2, 1])
        sku = c1.text_input("Código SKU", placeholder="Ej: PROD-001")
        nombre = c2.text_input("Nombre del Producto")
        venc = c3.date_input("Vencimiento")
        
        # Bloque de Logística
        c4, c5, c6 = st.columns(3)
        prov = c4.text_input("Proveedor")
        stock = c5.number_input("Stock Inicial", min_value=0)
        alerta = c6.number_input("Alerta Stock Mínimo", min_value=0)
        
        st.markdown("---")
        st.subheader("💰 Estructura de Precios")
        
        # Bloque de Precios (Diseño fraccionado)
        col_detal, col_bulto, col_mayor = st.columns(3)
        with col_detal:
            st.markdown("*1. Al Detal*")
            m_detal = st.number_input("Margen (%)", key="m_detal")
        with col_bulto:
            st.markdown("*2. Por Bulto*")
            m_bulto = st.number_input("Margen (%)", key="m_bulto")
        with col_mayor:
            st.markdown("*3. Al Mayor*")
            m_mayor = st.number_input("Margen (%)", key="m_mayor")
            
        # Bloque Fiscal y Comisión
        c_fiscal, c_vendedor = st.columns(2)
        iva = c_fiscal.selectbox("Impuesto Legal", ["General (16%)", "Exento"])
        vendedor = c_vendedor.text_input("Vendedor (Opcional)")
        
        st.file_uploader("Cargar Imagen para Catálogo", type=['jpg', 'png'])
        
        if st.button("🚀 GUARDAR REGISTRO", type="primary"):
            st.success("Producto guardado exitosamente.")
