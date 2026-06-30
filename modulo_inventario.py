import streamlit as st

def mostrar_formulario_inventario():
    st.markdown("## 📦 CARGA MAESTRA DE PRODUCTOS")
    
    with st.form("form_inventario_pro"):
        # --- SECCIÓN 1: DATOS BÁSICOS ---
        st.subheader("📝 1. Identificación del Producto")
        c1, c2, c3 = st.columns(3)
        sku = c1.text_input("Código SKU")
        nombre = c2.text_input("Nombre del Producto")
        vencimiento = c3.date_input("Fecha de Vencimiento")
        
        # --- SECCIÓN 2: ESTRUCTURA DE COSTOS Y BLINDAJE ---
        st.markdown("---")
        st.subheader("💰 2. Estructura de Costos y Blindaje (Binance)")
        f1, f2, f3 = st.columns(3)
        costo_base = f1.number_input("Costo Base ($)", min_value=0.0, format="%.2f")
        moneda = f2.selectbox("Moneda de Pago", ["USDT (Binance)", "USD (Efectivo)"])
        margen_blindaje = f3.slider("Margen Blindaje (%)", 0, 30, 5) # Slider para blindaje
        
        # --- SECCIÓN 3: ESTRATEGIA DE PRECIOS ---
        st.markdown("---")
        st.subheader("📊 3. Escala de Precios (Rentabilidad)")
        # Aplicamos la jerarquía: Detal > Bulto > Mayor
        p1, p2, p3 = st.columns(3)
        p1.number_input("Margen Detal (%)", min_value=0.0) # El más alto
        p2.number_input("Margen Bulto (%)", min_value=0.0) # Medio
        p3.number_input("Margen Mayor (%)", min_value=0.0) # El más bajo (mayor rentabilidad cliente)
        
        # --- SECCIÓN 4: GESTIÓN DE VENTAS ---
        st.markdown("---")
        st.subheader("🤝 4. Gestión de Ventas")
        comision = st.number_input("Comisión Vendedor (%)", min_value=0.0, max_value=20.0)
        
        # Acción final
        if st.form_submit_button("🚀 REGISTRAR Y BLINDAR CAPITAL"):
            # Aquí irá la lógica de cálculo automático basada en tus márgenes
            st.success("Producto registrado y precios anclados.")
            st.rerun()
