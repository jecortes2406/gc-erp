import streamlit as st

st.set_page_config(layout="wide", page_title="ERP Maestro")

st.markdown("""
    <style>
    /* Fondo Gris Medio Corporativo */
    .stApp { background-color: #f1f3f4; }
    /* Estilo de Tarjetas */
    .css-1r6slb0, .stForm { 
        background-color: white; 
        border-radius: 12px; 
        padding: 24px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        border: 1px solid #e0e0e0;
    }
    /* Tipografía y Contraste */
    h1, h2, h3 { color: #202124; font-weight: 600; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0; }
    </style>
""", unsafe_allow_html=True)
