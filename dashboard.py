import streamlit as st
import pandas as pd

def render_dashboard():
    st.markdown("# 📊 PANEL DE CONTROL EJECUTIVO")
    
    # Verificación de datos
    if 'db_inventario' not in st.session_state or st.session_state.db_inventario.empty:
        st.warning("No hay datos en la matriz para calcular los KPIs. Registra productos primero.")
        return

    df = st.session_state.db_inventario
    
    # 1. KPIs DE SALUD FINANCIERA (Inversión vs Proyección)
    total_inversion = df['Costo USD'].sum()
    # Asumimos que precio sugerido es el de venta
    total_venta_estimada = df['Precio Venta (Bs)'].sum() 
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Inversión Total (USD)", f"$ {total_inversion:,.2f}")
    c2.metric("Valor Total Venta (Bs)", f"Bs. {total_venta_estimada:,.2f}")
    c3.metric("Margen Promedio", f"{df['Margen %'].mean():.1f} %")

    st.markdown("---")

    # 2. PORTAFOLIO POR CATEGORÍA
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📦 Portafolio por Categoría")
        cat_data = df.groupby('Categoría')['Producto'].count()
        st.bar_chart(cat_data)
        
    with col_b:
        st.subheader("💰 Distribución de Márgenes")
        st.line_chart(df[['Producto', 'Margen %']].set_index('Producto'))

    # 3. ALERTA DE PUNTO DE EQUILIBRIO
    st.markdown("---")
    st.subheader("📈 Proyección de Industria")
    
    # Lógica simple: Si el margen promedio es menor a un umbral, alerta
    if df['Margen %'].mean() < 20:
        st.error("⚠️ Alerta: El margen promedio es bajo (< 20%). Ajuste de precios sugerido.")
    else:
        st.success("✅ Salud financiera: Margen promedio operativo óptimo.")
