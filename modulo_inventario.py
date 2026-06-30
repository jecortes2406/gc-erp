import streamlit as st
import pandas as pd
import sqlite3

# --- LÓGICA DE NEGOCIO ---
def obtener_inventario():
    conn = sqlite3.connect('inventario.db')
    try:
        # Consulta explícita para evitar errores de mapeo
        query = "SELECT sku, nombre, categoria, costo_base, margen_detal, iva_aplicado, comision_vendedor FROM productos"
        df = pd.read_sql_query(query, conn)
        # Renombramos para visualización profesional
        df.columns = ["SKU", "Producto", "Categoría", "Costo ($)", "Margen (%)", "IVA (%)", "Comisión (%)"]
    except:
        df = pd.DataFrame(columns=["SKU", "Producto", "Categoría", "Costo ($)", "Margen (%)", "IVA (%)", "Comisión (%)"])
    conn.close()
    return df

# --- INTERFAZ PROFESIONAL ---
def mostrar_formulario_inventario():
    st.markdown("## 📦 INVENTARIO MAESTRO")
    
    # Manejo de estado para navegación fluida
    if 'modo_ingreso' not in st.session_state: st.session_state.modo_ingreso = False

    if not st.session_state.modo_ingreso:
        # VISTA DE DASHBOARD
        col1, col2 = st.columns([0.85, 0.15])
        col1.subheader("Listado de Existencias")
        if col2.button("＋ AGREGAR"):
            st.session_state.modo_ingreso = True
            st.rerun()
            
        st.dataframe(obtener_inventario(), use_container_width=True, hide_index=True)
    else:
        # VISTA DE FORMULARIO
        st.subheader("📝 Carga de Nuevo Producto")
        with st.form("form_inventario", clear_on_submit=True):
            c1, c2 = st.columns(2)
            sku = c1.text_input("Código SKU")
            nombre = c2.text_input("Nombre del Producto")
            
            c3, c4, c5 = st.columns(3)
            costo = c3.number_input("Costo Base ($)", min_value=0.0)
            margen = c4.number_input("Margen Detal (%)", min_value=0.0)
            iva = c5.selectbox("IVA (%)", [0, 8, 16])
            
            comision = st.number_input("Comisión Vendedor (%)", min_value=0.0)
            
            if st.form_submit_button("💾 GUARDAR PRODUCTO"):
                # Aquí iría tu función de INSERT INTO
                st.success("Producto registrado exitosamente.")
                st.session_state.modo_ingreso = False
                st.rerun()
        
        if st.button("⬅️ Volver al Dashboard"):
            st.session_state.modo_ingreso = False
            st.rerun()
