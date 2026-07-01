import streamlit as st
import pandas as pd
import os

FILES = {
    'db_inventario': 'data_inventario.csv',
    'db_ventas': 'data_ventas.csv',
    'db_contable': 'data_contable.csv'
}

def init_db():
    for key, filename in FILES.items():
        if key not in st.session_state:
            if os.path.exists(filename):
                st.session_state[key] = pd.read_csv(filename)
            else:
                # Si el archivo no existe, creamos un DataFrame vacío
                st.session_state[key] = pd.DataFrame() 
                st.session_state[key].to_csv(filename, index=False)

def save_data(key):
    """Guarda el DataFrame actual en el archivo CSV correspondiente."""
    if key in st.session_state:
        st.session_state[key].to_csv(FILES[key], index=False)
