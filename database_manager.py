import streamlit as st
import pandas as pd
import os

FILES = {
    'db_inventario': 'data_inventario.csv',
    'db_ventas': 'data_ventas.csv'
}

def init_db():
    # Carga los archivos desde el disco duro
    for key, filename in FILES.items():
        if key not in st.session_state:
            if os.path.exists(filename):
                st.session_state[key] = pd.read_csv(filename)
            else:
                # Estructura inicial si no hay archivo
                if key == 'db_inventario':
                    st.session_state[key] = pd.DataFrame(columns=['Código', 'Producto', 'Precio'])
                else:
                    st.session_state[key] = pd.DataFrame(columns=['Producto', 'Cantidad', 'Total'])
                st.session_state[key].to_csv(filename, index=False)

def save_data(key):
    # Escribe el cambio al disco inmediatamente
    st.session_state[key].to_csv(FILES[key], index=False)
