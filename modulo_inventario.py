import streamlit as st
from database_manager import agregar_producto

def mostrar_formulario_inventario():
    st.subheader("📦 Formulario Maestro de Carga de Productos")
    
    with st.form("form_producto"):
        nombre = st.text_input("Nombre del Producto")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            costo = st.number_input("Costo Adquisición", min_value=0.0, format="%.2f")
            moneda = st.selectbox("Moneda", ["Binance", "Euro", "Bolívar"])
        
        with col2:
            margen_detal = st.number_input("Margen Detal (%)", 0.0)
            margen_bulto = st.number_input("Margen Bulto (%)", 0.0)
            margen_mayor = st.number_input("Margen Mayor (%)", 0.0)
            
        with col3:
            comision_detal = st.number_input("Comisión Detal (%)", 0.0)
            comision_bulto = st.number_input("Comisión Bulto (%)", 0.0)
            comision_mayor = st.number_input("Comisión Mayor (%)", 0.0)
            
        submit = st.form_submit_button("Registrar Producto en Sistema")
        
        if submit:
            # Aquí capturamos la tasa actual del estado global
            tasa_actual = st.session_state.get('tasa_binance', 1.0)
            datos = (nombre, costo, moneda, tasa_actual, margen_detal, margen_bulto, 
                     margen_mayor, comision_detal, comision_bulto, comision_mayor)
            
            agregar_producto(datos)
            st.success(f"Producto {nombre} registrado con éxito en el motor central.")

# Para visualizarlo, llamarás a esta función desde app.py
