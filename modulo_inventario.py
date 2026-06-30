import streamlit as st
import pandas as pd
import sqlite3

# Inicializar estado para controlar la vista (Dashboard vs Formulario)
if 'mostrar_form_ingreso' not in st.session_state:
    st.session_state.mostrar_form_ingreso = False

def obtener_datos_inventario():
    conn = sqlite3.connect('inventario.db')
    try:
        df = pd.read_sql_query("SELECT * FROM productos", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df

def mostrar_formulario_inventario():
    st.subheader("📦 INVENTARIO MAESTRO")
    
    # Si NO estamos en modo ingreso, mostramos el Dashboard (Tabla + Botón)
    if not st.session_state.mostrar_form_ingreso:
        df = obtener_datos_inventario()
        
        # Fila de KPIs (Resumen ejecutivo)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("VALOR VENTA", "$0.00")
        col2.metric("STOCK BAJO", "0")
        col3.metric("UNIDADES", str(df['existencia_detal'].sum() if not df.empty else 0))
        col4.metric("INVERSIÓN", "$0.00")

        st.markdown("---")

        if st.button("＋ NUEVO INGRESO", type="primary"):
            st.session_state.mostrar_form_ingreso = True
            st.rerun()

        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No hay productos registrados. Presiona 'Nuevo Ingreso'.")

    # Si SÍ estamos en modo ingreso, mostramos el formulario
    else:
        st.subheader("📝 Registro de Nuevo Producto")
        # Aquí es donde irá tu formulario detallado que diseñaremos paso a paso
        if st.button("⬅️ Volver al Inventario"):
            st.session_state.mostrar_form_ingreso = False
            st.rerun()
