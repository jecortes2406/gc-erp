import streamlit as st
import pandas as pd
import os

# Nombres de los archivos que serán tu respaldo real
FILES = {
    'db_inventario': 'data_inventario.csv',
    'db_ventas': 'data_ventas.csv',
    'db_contable': 'data_contable.csv'
}

def init_db():
    # Cargar o crear las bases de datos desde disco
    for key, filename in FILES.items():
        if key not in st.session_state:
            if os.path.exists(filename):
                st.session_state[key] = pd.read_csv(filename)
            else:
                # Definición de estructuras iniciales si no existen
                if key == 'db_inventario':
                    st.session_state[key] = pd.DataFrame(columns=['Código', 'Producto', 'Categoría', 'Costo USD', 'Margen %', 'Comisión %', 'Precio Venta (Bs)'])
                elif key == 'db_ventas':
                    st.session_state[key] = pd.DataFrame(columns=['Producto', 'Cantidad', 'Total Bs', 'Comisión', 'Vendedor'])
                else:
                    st.session_state[key] = pd.DataFrame(columns=['Fecha', 'Tipo', 'Concepto', 'Categoría', 'Monto Original', 'Moneda', 'Tasa Aplicada', 'Monto USD'])
                
                # Guardar el archivo vacío por primera vez
                st.session_state[key].to_csv(filename, index=False)

def save_data(key):
    # Función para persistir cambios en disco inmediatamente
    st.session_state[key].to_csv(FILES[key], index=False)
