import streamlit as st

def mostrar_formulario_inventario():
    # DASHBOARD DE INVENTARIO
    st.markdown("## 📈 DASHBOARD DE INVENTARIO")
    
    # 1. KPIs DE MEDICIÓN (Métricas de Punta)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Inversión Total", "$0.00")
    k2.metric("Ganancia Proyectada", "$0.00")
    k3.metric("Gastos Acumulados", "$0.00")
    k4.metric("Almacenes", "Principal")
    
    st.markdown("---")
    
    # 2. ACCIÓN PRINCIPAL
    if st.button("＋ AGREGAR NUEVO PRODUCTO"):
        st.session_state.modo_ingreso = True
        st.rerun()

    # 3. LISTADO MAESTRO
    st.subheader("Listado de Existencias")
    st.write("Aquí se visualizará la tabla profesional con todas las columnas descritas.")

# Lógica del formulario (se activará con el botón)
def renderizar_formulario():
    with st.form("form_pro"):
        st.subheader("Detalles del Producto")
        # Filas estructuradas
        c1, c2 = st.columns(2)
        c1.text_input("Código SKU")
        c2.text_input("Nombre del Producto")
        
        c3, c4 = st.columns(2)
        c3.number_input("Costo Base", format="%.2f")
        c4.selectbox("Moneda", ["USD", "USDT"])
        
        st.markdown("### Estrategia de Precios")
        p1, p2, p3 = st.columns(3)
        p1.number_input("Margen Detal (%)")
        p2.number_input("Margen Bulto (%)")
        p3.number_input("Margen Mayor (%)")
        
        st.markdown("### Gestión de Comisiones")
        st.number_input("Porcentaje Comisión Vendedor (%)", min_value=0.0, max_value=100.0)
        
        st.form_submit_button("GUARDAR EN BASE DE DATOS")
