import streamlit as st
import pandas as pd

def init_db():
    # Inicialización de tablas si no existen
    if 'db_inventario' not in st.session_state:
        st.session_state.db_inventario = pd.DataFrame(columns=['Código', 'Producto', 'Costo USD', 'Precio Venta'])
    if 'db_ventas' not in st.session_state:
        st.session_state.db_ventas = pd.DataFrame(columns=['Producto', 'Cantidad', 'Total'])
    if 'db_contable' not in st.session_state:
        st.session_state.db_contable = pd.DataFrame(columns=['Fecha', 'Concepto', 'Monto', 'Tipo'])
