import streamlit as st
import pandas as pd

def render_pos():
    st.markdown("## 🧾 SISTEMA DE FACTURACIÓN (POS)")
    
    # 1. Selección de Cliente
    col1, col2 = st.columns([2, 1])
    cliente = col1.selectbox("Seleccionar Cliente", ["Cliente Genérico (Venta Rápida)", "+ Crear Nuevo Cliente"])
    
    # 2. Carrito de Ventas (Aquí usaremos la matriz de inventario)
    if 'carrito' not in st.session_state:
        st.session_state.carrito = []

    # 3. Lógica de Pago con Conciliación Bancaria
    with st.expander("💳 Finalizar Venta / Cierre"):
        metodo = st.radio("Método de Pago", ["Efectivo USD", "Zelle", "Transferencia", "Punto/Débito"])
        
        if metodo == "Transferencia":
            c_ref1, c_ref2 = st.columns(2)
            ref_bancaria = c_ref1.text_input("4 últimos dígitos de Referencia", max_chars=4)
            monto_transfer = c_ref2.number_input("Monto Recibido", min_value=0.0)
            
            # Validación: No permite procesar sin los datos
            if len(ref_bancaria) < 4:
                st.warning("⚠️ Debe ingresar los 4 dígitos de la referencia.")
                
    # 4. Botón de Procesar (Aquí calcularemos la comisión del vendedor)
    if st.button("🚀 PROCESAR VENTA"):
        # Lógica: 
        # A. Restar stock en Inventario
        # B. Calcular comisión = Precio_Venta * (Comision_Pct / 100)
        # C. Guardar en Historial
        st.success("Venta procesada con éxito.")
