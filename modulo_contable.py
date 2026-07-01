import streamlit as st
import pandas as pd
from datetime import datetime

def render_modulo_contable():
    st.markdown("## 📊 MÓDULO CONTABLE Y FLUJO DE CAJA")
    
    # 1. Inicialización de datos contables
    if 'db_contable' not in st.session_state:
        st.session_state.db_contable = pd.DataFrame(columns=[
            'Fecha', 'Tipo', 'Concepto', 'Categoría', 'Monto Original', 'Moneda', 'Tasa Aplicada', 'Monto USD'
        ])

    # 2. Formulario de Registro
    with st.form("registro_contable", clear_on_submit=True):
        col1, col2 = st.columns(2)
        tipo = col1.selectbox("Tipo de Movimiento", ["Egreso", "Ingreso"])
        categoria = col2.selectbox("Categoría", ["Alquiler", "Servicios", "Nómina", "Impuestos", "Ventas", "Otros"])
        
        concepto = st.text_input("Concepto (Descripción)")
        
        c3, c4 = st.columns(2)
        monto = c3.number_input("Monto", min_value=0.0, format="%.2f")
        moneda = c4.selectbox("Moneda", ["USD", "Bs"])
        
        if st.form_submit_button("💾 REGISTRAR MOVIMIENTO"):
            # Lógica de conversión
            tasa = st.session_state.get('tasa_binance', 1.0)
            monto_usd = monto if moneda == "USD" else (monto / tasa)
            
            nuevo_registro = pd.DataFrame([{
                'Fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'Tipo': tipo,
                'Concepto': concepto,
                'Categoría': categoria,
                'Monto Original': monto,
                'Moneda': moneda,
                'Tasa Aplicada': tasa,
                'Monto USD': monto_usd
            }])
            
            st.session_state.db_contable = pd.concat([st.session_state.db_contable, nuevo_registro], ignore_index=True)
            st.success("Movimiento contable registrado y convertido a USD.")

    # 3. Visualización y Resumen
    st.subheader("📋 Estado de Resultados / Caja")
    if not st.session_state.db_contable.empty:
        st.dataframe(st.session_state.db_contable, use_container_width=True)
        
        # Resumen Rápido
        total_ingresos = st.session_state.db_contable[st.session_state.db_contable['Tipo'] == 'Ingreso']['Monto USD'].sum()
        total_egresos = st.session_state.db_contable[st.session_state.db_contable['Tipo'] == 'Egreso']['Monto USD'].sum()
        
        c_r1, c_r2, c_r3 = st.columns(3)
        c_r1.metric("Total Ingresos (USD)", f"$ {total_ingresos:,.2f}")
        c_r2.metric("Total Egresos (USD)", f"$ {total_egresos:,.2f}")
        c_r3.metric("Balance Neto (USD)", f"$ {(total_ingresos - total_egresos):,.2f}")
    else:
        st.info("Sin movimientos registrados.")
