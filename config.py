import streamlit as st

def init_config():
    """
    Inicializa las variables globales del sistema en la sesión.
    Esto permite que las tasas sean accesibles desde cualquier módulo
    (inventario, ventas, compras) sin perder el valor.
    """
    if 'tasas' not in st.session_state:
        # Aquí se definen los valores iniciales para tu anclaje a Binance/BCV
        st.session_state.tasas = {
            'BCV': 36.50, 
            'BINANCE': 37.10, 
            'EURO': 40.20
        }
    
    if 'usuario' not in st.session_state:
        st.session_state.usuario = {
            'nombre': 'jecortes',
            'cargo': 'ADMINISTRADOR',
            'estado': 'ACTIVO'
        }

def get_tasas():
    """Retorna las tasas actuales para cálculos contables."""
    return st.session_state.tasas
