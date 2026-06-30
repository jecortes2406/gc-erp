import streamlit as st
import pandas as pd
import sqlite3

# Función para obtener los productos de la base de datos
def obtener_datos_inventario():
    conn = sqlite3.connect('inventario.db')
    df = pd.read_sql_query("SELECT * FROM productos", conn)
    conn.close()
    return df

def mostrar_formulario_inventario():
    st.subheader("📦 INVENTARIO MAESTRO")
    st.caption("Auditoría profesional de almacén - Proyecto Grupo Comercial")

    # 1. Dashboard de KPIs (Resumen Ejecutivo)
    df = obtener_datos_inventario()
    
    col1, col2, col3, col4 = st.columns(4)
    # Ejemplo de cálculos rápidos (se ajustarán cuando cargues datos)
    col1.metric("VALOR VENTA TOTAL", "$0.00")
    col2.metric("STOCK BAJO", "0")
    col3.metric("UNIDADES", str(df['existencia_detal'].sum() if not df.empty else 0))
    col4.metric("INVERSIÓN", "$0.00")

    st.markdown("---")

    # 2. Botón de Nuevo Ingreso
    if st.button("＋ NUEVO INGRESO", type="primary"):
        st.session_state.mostrar_form_ingreso = True

    # 3. Tabla de Productos (Tu centro de mando)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay productos en inventario. ¡Carga el primero!")

    # 4. Lógica de despliegue del formulario (se activará si presionas el botón)
    if st.session_state.get('mostrar_form_ingreso', False):
        st.subheader("Registro de Nuevo Producto")
        # Aquí irá el formulario detallado que diseñamos previamente
        if st.button("Cerrar Formulario"):
            st.session_state.mostrar_form_ingreso = False
            st.rerun()
