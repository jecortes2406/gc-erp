import streamlit as st

def mostrar_formulario_inventario():
    st.markdown("## 📦 GESTIÓN DE INVENTARIO MAESTRO")
    
    if 'modo_ingreso' not in st.session_state: st.session_state.modo_ingreso = False

    if not st.session_state.modo_ingreso:
        # Aquí se mantiene tu Dashboard y botón de agregar
        if st.button("＋ AGREGAR NUEVO PRODUCTO", type="primary"):
            st.session_state.modo_ingreso = True
            st.rerun()
        st.write("---")
        st.write("### Listado de Existencias")
        # Aquí va tu tabla existente...
        
    else:
        # --- NUEVO ESQUEMA INTEGRADO ---
        with st.form("form_inventario_pro"):
            st.subheader("📝 Carga de Producto")
            
            # Bloque 1: Identificación
            c1, c2 = st.columns(2)
            sku = c1.text_input("Código SKU")
            nombre = c2.text_input("Nombre del Producto")
            
            # Bloque 2: Costos (El corazón financiero)
            st.markdown("---")
            st.markdown("### 💰 Estructura de Costos")
            f1, f2, f3 = st.columns(3)
            costo = f1.number_input("Costo Base ($)", min_value=0.0, format="%.2f")
            moneda = f2.selectbox("Moneda", ["USD", "USDT"])
            comision = f3.number_input("Comisión Vendedor (%)", min_value=0.0)
            
            # Bloque 3: Niveles de Venta (Los 3 precios)
            st.markdown("---")
            st.markdown("### 📊 Niveles de Venta (Márgenes)")
            n1, n2, n3 = st.columns(3)
            margen_detal = n1.number_input("Margen Detal (%)", 0.0)
            margen_bulto = n2.number_input("Margen Bulto (%)", 0.0)
            margen_mayor = n3.number_input("Margen Mayor (%)", 0.0)
            
            # Botón de acción
            if st.form_submit_button("💾 GUARDAR PRODUCTO"):
                st.success("Producto registrado exitosamente con sus estructuras de precio.")
                st.session_state.modo_ingreso = False
                st.rerun()
        
        if st.button("⬅️ Volver al listado"):
            st.session_state.modo_ingreso = False
            st.rerun()
