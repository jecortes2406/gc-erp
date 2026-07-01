import streamlit as st

def render_dashboard():
    st.markdown("# 📊 PANEL DE CONTROL")
    
    # Selector de tipo de vista
    vista = st.selectbox("Seleccionar vista de análisis", 
                         ["Resumen Ejecutivo", "Análisis de Ventas", "Salud Financiera", "Inventario"])
    
    if vista == "Resumen Ejecutivo":
        c1, c2, c3 = st.columns(3)
        c1.metric("Venta Total (Mes)", "$ 12,450", "+12%")
        c2.metric("Margen Real", "32%", "-1%")
        c3.metric("Capital en Stock", "$ 45,000", "Estable")
        
    elif vista == "Salud Financiera":
        st.subheader("Estructura de Costos y Protección")
        # Aquí irán los gráficos de barras de tus gastos vs ganancias
        st.line_chart([100, 120, 115, 140]) # Ejemplo de tendencia
