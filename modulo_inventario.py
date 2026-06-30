import streamlit as st
import pandas as pd
import sqlite3

def mostrar_formulario_inventario():
    # Inicializar estado si no existe
    if 'mostrar_form_ingreso' not in st.session_state:
        st.session_state.mostrar_form_ingreso = False

    st.subheader("📦 INVENTARIO MAESTRO")
    
    # Dashboard de KPIs (Fila superior)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("VALOR VENTA TOTAL", "$0.00")
    col2.metric("STOCK BAJO", "0")
    col3.metric("UNIDADES", "0")
    col4.metric("INVERSIÓN", "$0.00")

    st.markdown("---")

    # Botón de control maestro
    if st.button("＋ NUEVO INGRESO", type="primary"):
        st.session_state.mostrar_form_ingreso = True
        st.rerun()

    # Lógica de renderizado
    if st.session_state.mostrar_form_ingreso:
        st.subheader("Registrar Nuevo Producto")
        # Aquí irá el formulario que diseñamos
        if st.button("⬅️ Volver al Inventario"):
            st.session_state.mostrar_form_ingreso = False
            st.rerun()
    else:
        # Aquí mostramos la tabla cuando no estamos ingresando nada
        st.write("Tabla de productos existente (Vacía actualmente)")
