import streamlit as st
import pandas as pd
import sqlite3

# Importamos las funciones necesarias desde tu gestor de base de datos existente
from database_manager import obtener_inventario 

# --- FUNCIONES DE BASE DE DATOS ---
def guardar_producto(datos):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    # Usamos INSERT OR REPLACE para que no falle si intentan actualizar un SKU existente
    cursor.execute('''INSERT OR REPLACE INTO productos (sku, nombre, categoria, costo_base, moneda_compra, almacen, 
                      margen_detal, margen_bulto, margen_mayor, existencia_bulto, existencia_detal, 
                      iva_aplicado, comision_vendedor) 
                      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', tuple(datos.values()))
    conn.commit()
    conn.close()

# --- INTERFAZ DEL MÓDULO ---
def mostrar_formulario_inventario():
    st.subheader("📋 GESTIÓN DE INVENTARIO - LISTADO MAESTRO")
    
    if 'modo_ingreso' not in st.session_state: 
        st.session_state.modo_ingreso = False

    if not st.session_state.modo_ingreso:
        # VISTA DE LISTA PROFESIONAL
        df = obtener_inventario() 
        
        col_btn, col_vacio = st.columns([0.2, 0.8])
        if col_btn.button("＋ NUEVO PRODUCTO", type="primary"):
            st.session_state.modo_ingreso = True
            st.rerun()
            
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Inventario vacío. Comienza agregando productos.")

    else:
        # FORMULARIO DE CARGA PROFESIONAL
        st.markdown("### 📝 Configuración de Producto")
        
        # Creamos una columna para el botón de regresar arriba del formulario como alternativa segura
        if st.button("⬅️ Volver al Listado", key="btn_volver_arriba"):
            st.session_state.modo_ingreso = False
            st.rerun()
            
        with st.form("form_producto_completo"):
            # Sección 1: Identificación
            c1, c2, c3 = st.columns(3)
            sku = c1.text_input("SKU")
            nombre = c2.text_input("Nombre")
            cat = c3.selectbox("Categoría", ["Víveres", "Limpieza", "Hogar", "Otros"])
            
            # Sección 2: Costos y Márgenes
            st.markdown("---")
            st.markdown("#### 💰 Márgenes y Precios")
            m1, m2, m3 = st.columns(3)
            costo = m1.number_input("Costo Base", min_value=0.0)
            margen_detal = m2.number_input("Margen Detal (%)", 0.0)
            margen_mayor = m3.number_input("Margen Mayor (%)", 0.0)
            
            # Sección 3: Impuestos y Comisiones
            st.markdown("---")
            st.markdown("#### ⚖️ Impuestos y Comisiones")
            i1, i2 = st.columns(2)
            iva = i1.selectbox("IVA Aplicado", [0, 8, 16], format_func=lambda x: f"{x}%")
            comision = i2.number_input("Comisión Vendedor (%)", min_value=0.0, step=0.5)
            
            # Sección de Acciones del Formulario
            st.markdown(" <br> ", unsafe_allow_html=True)
            col_enviar, col_limpiar = st.columns([0.2, 0.8])
            
            guardar = col_enviar.form_submit_button("💾 Guardar Producto")
            
            if guardar:
                if not sku.strip() or not nombre.strip():
                    st.error("⚠️ El SKU y el Nombre son campos obligatorios obligatorios para el sistema.")
                else:
                    datos = {'sku': sku, 'nom': nombre, 'cat': cat, 'costo': costo, 'mon': 'USD', 
                             'alm': 'Principal', 'md': margen_detal, 'mb': 0, 'mm': margen_mayor, 
                             'eb': 0, 'ed': 0, 'iva': iva, 'com': comision}
                    guardar_producto(datos)
                    st.session_state.modo_ingreso = False
                    st.rerun()
