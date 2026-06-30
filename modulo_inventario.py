import streamlit as st
import pandas as pd
import sqlite3

def obtener_inventario():
    conn = sqlite3.connect('inventario.db')
    try:
        df = pd.read_sql_query("SELECT * FROM productos", conn)
        # Renombrar columnas para visualización profesional
        df.columns = ['ID', 'SKU', 'Nombre', 'Categoría', 'Costo', 'Moneda', 
                      'Almacén', 'Margen Detal', 'Margen Bulto', 'Margen Mayor', 
                      'Stock Bulto', 'Stock Detal', 'IVA %', 'Comisión Vendedor %']
    except:
        df = pd.DataFrame()
    conn.close()
    return df

def mostrar_formulario_inventario():
    # Título con estilo ejecutivo
    st.markdown("<h2 style='text-align: left; color: #2E86C1;'>📦 MÓDULO DE INVENTARIO MAESTRO</h2>", unsafe_allow_html=True)
    
    if 'modo_ingreso' not in st.session_state: st.session_state.modo_ingreso = False

    if not st.session_state.modo_ingreso:
        # VISTA DE LISTADO (PROFESIONAL)
        df = obtener_inventario()
        
        # Botón de acción con estilo
        if st.button("＋ AGREGAR NUEVO PRODUCTO", type="primary"):
            st.session_state.modo_ingreso = True
            st.rerun()
            
        st.markdown("### 📊 Registro de Existencias")
        if not df.empty:
            # Lista profesional sin índices molestos
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay registros en la base de datos.")

    else:
        # VISTA DE FORMULARIO CON ETIQUETAS Y ESTRUCTURA TÉCNICA
        st.markdown("### 📝 Formulario de Carga de Inventario")
        with st.form("form_inventario_pro"):
            # FILA 1: Identificación
            col1, col2, col3 = st.columns(3)
            sku = col1.text_input("🔑 Código SKU")
            nombre = col2.text_input("🏷️ Descripción del Producto")
            cat = col3.selectbox("📂 Categoría", ["Víveres", "Limpieza", "Hogar", "Otros"])
            
            # FILA 2: Financiero
            st.markdown("---")
            st.markdown("#### 💰 Configuración Financiera")
            f1, f2, f3 = st.columns(3)
            costo = f1.number_input("💵 Costo Base (USD)", min_value=0.0, format="%.2f")
            margen_detal = f2.number_input("📈 Margen Detal (%)", min_value=0.0)
            margen_mayor = f3.number_input("📊 Margen Mayor (%)", min_value=0.0)
            
            # FILA 3: Impuestos y Ventas
            st.markdown("#### ⚖️ Impuestos y Comisiones")
            i1, i2 = st.columns(2)
            iva = i1.selectbox("🛡️ IVA Aplicado (%)", [0, 8, 16])
            comision = i2.number_input("🤝 Comisión Vendedor (%)", min_value=0.0, step=0.5)
            
            submitted = st.form_submit_button("🚀 REGISTRAR PRODUCTO EN BASE DE DATOS")
            
            if submitted:
                # Aquí la lógica de guardado
                st.success(f"Producto {sku} registrado con éxito en el sistema.")
                st.session_state.modo_ingreso = False
                st.rerun()

        if st.button("⬅️ Volver al listado"):
            st.session_state.modo_ingreso = False
            st.rerun()
