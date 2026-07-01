import streamlit as st

@st.cache_data(ttl=3600)
def obtener_tasas():
    # Retorna (Tasa Binance, Tasa BCV)
    return 46.50, 765.00
