import streamlit as st
import pandas as pd

def init_db():
    # Inicialización centralizada para que ningún módulo falle
    if 'db_inventario' not in st.session_state:
        st.session_state.db_inventario = pd.DataFrame(columns=[
            'Código', 'Producto', 'Categoría', 'Costo USD', 'Precio Detal', 'Precio Mayor', 'Stock'
        ])
    return st.session_state.db_inventario
