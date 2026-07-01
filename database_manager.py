import streamlit as st
import pandas as pd

def init_db():
    if 'db_inventario' not in st.session_state:
        st.session_state.db_inventario = pd.DataFrame(columns=[
            'Código', 'Producto', 'Categoría', 'Costo USD', 'Margen %', 'Comisión %', 'Precio Venta (Bs)'
        ])
    if 'db_ventas' not in st.session_state:
        st.session_state.db_ventas = pd.DataFrame()
    return st.session_state.db_inventario
