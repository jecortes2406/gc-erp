import streamlit as st

def run():
    st.markdown("## 🏢 GESTIÓN DE INVENTARIO")
    
    # Usamos la clase .card-white definida en tu app.py
    with st.container():
        st.markdown('<div class="card-white">', unsafe_allow_html=True)
        st.subheader("📝 NUEVO PRODUCTO")
        
        c1, c2 = st.columns(2)
        sku = c1.text_input("Código SKU")
        nombre = c2.text_input("Nombre del Producto")
        
        c3, c4, c5 = st.columns(3)
        costo = c3.number_input("Costo (USD)")
        precio_detal = c4.number_input("Precio Detal (USD)")
        precio_mayor = c5.number_input("Precio Mayor (USD)")
        
        if st.button("🚀 GUARDAR EN BASE DE DATOS", type="primary"):
            st.success("Producto registrado anclado a Binance.")
        st.markdown('</div>', unsafe_allow_html=True)
