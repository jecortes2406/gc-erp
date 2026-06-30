import streamlit as st
from database_manager import agregar_producto

def mostrar_formulario_inventario():
    st.subheader("📦 Formulario Maestro de Carga de Productos")
    
    # Abrimos el formulario con un diseño limpio
    with st.form("form_producto_pro"):
        # SECCIÓN 1: Identificación y Clasificación
        st.markdown("### 1. Información del Producto")
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre / Descripción del Producto")
            categoria = st.selectbox("Categoría", ["Víveres", "Confitería", "Heladería", "Hogar", "Limpieza"])
        with col2:
            codigo = st.text_input("Código de Producto (SKU)")
            almacen = st.radio("Almacén de Ubicación", ["Principal", "Secundario"], horizontal=True)
            
        # SECCIÓN 2: Costos y Valoración
        st.markdown("### 2. Estructura de Costos")
        c1, c2 = st.columns(2)
        with c1:
            costo = st.number_input("Costo de Adquisición (Base)", min_value=0.0, format="%.2f")
        with c2:
            moneda = st.selectbox("Moneda de Compra", ["Binance (USDT)", "Euro", "Bolívar (VES)"])
            
        # SECCIÓN 3: Matriz de Márgenes y Comisiones
        st.markdown("### 3. Matriz de Márgenes y Comisiones")
        cols = st.columns(3)
        etiquetas = ["Detal", "Bulto", "Mayor"]
        
        # Diccionarios para almacenar los valores dinámicos
        márgenes = {}
        comisiones = {}
        
        for i, tipo in enumerate(etiquetas):
            with cols[i]:
                st.write(f"*Nivel: {tipo}*")
                márgenes[tipo] = st.number_input(f"Margen {tipo} (%)", 0.0, key=f"m_{tipo}")
                comisiones[tipo] = st.number_input(f"Comisión {tipo} (%)", 0.0, key=f"c_{tipo}")

        # Botón de acción con estilo
        submit = st.form_submit_button("Guardar Producto en Base de Datos")
        
        if submit:
            st.success(f"Producto '{nombre}' ({codigo}) clasificado en {categoria} - Almacén: {almacen}")
            # Próximamente: integraremos la función insertar_producto con estos datos
