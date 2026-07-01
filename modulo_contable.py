import streamlit as st
import pandas as pd
from datetime import datetime
# IMPORTANTE: Aquí agregas save_data a la importación
from database_manager import init_db, save_data 

def render_modulo_contable():
    st.markdown("## 📊 MÓDULO CONTABLE")
    init_db() # Asegura que los datos estén cargados en memoria
    
    with st.form("registro_contable", clear_on_submit=True):
        # ... (tus campos de entrada) ...
        # ...
        
        if st.form_submit_button("💾 REGISTRAR MOVIMIENTO"):
            # ... tu lógica de cálculo de monto_usd ...
            
            nuevo_registro = pd.DataFrame([{
                'Fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
                # ... resto de campos ...
            }])
            
            # 1. Actualizas la memoria
