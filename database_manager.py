import streamlit as st
import pandas as pd
import sqlite3

# --- INICIALIZACIÓN DE LA BASE DE DATOS ---
def init_db():
    """Crea la tabla de productos si no existe con la estructura correcta."""
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            sku TEXT PRIMARY KEY,
            nombre TEXT,
            categoria TEXT,
            costo_base REAL,
            moneda_compra TEXT,
            almacen TEXT,
            margen_detal REAL,
            margen_bulto REAL,
            margen_mayor REAL,
            existencia_bulto INTEGER,
            existencia_detal INTEGER,
            iva_aplicado INTEGER,
            comision_vendedor REAL
        )
    ''')
    conn.commit()
    conn.close()

# --- FUNCIONES DE BASE DE DATOS ---
def obtener_inventario():
    """Recupera todos los productos de la base de datos."""
    conn = sqlite3.connect('inventario.db')
    try:
        df = pd.read_sql_query("SELECT * FROM productos", conn)
    except Exception:
        df = pd.DataFrame()
    conn.close()
    return df

def guardar_producto(datos):
    """Guarda un nuevo producto en la base de datos."""
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT OR REPLACE INTO productos (sku, nombre, categoria, costo_base, moneda_compra, almacen, 
                          margen_detal, margen_bulto, margen_mayor, existencia_bulto, existencia_detal, 
                          iva_aplicado, comision_vendedor) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', tuple(datos.values()))
        conn.commit()
        st.success("✅ ¡Producto guardado con éxito!")
    except Exception as e:
        st.error(f"❌ Error al guardar en la base de datos: {e}")
    finally:
        conn.close()

# --- INTERFAZ DEL MÓDULO ---
def mostrar_formulario_inventario():
    st.subheader("📋 GESTIÓN DE INVENTARIO - LISTADO MAESTRO")
    
    if 'modo_ingreso' not in st.session_state: 
        st.session_state.modo_ingreso = False

    if not st.session_state.modo_ingreso:
        # VISTA DE LISTADO
        df = obtener_inventario()
        
        col_btn, _ = st.columns([0.2, 0.8])
        if col_btn.button("＋ NUEVO PRODUCTO", type="primary"):
            st.session_state.modo_ingreso = True
            st.rerun()
            
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("El inventario está vacío. Presiona 'Nuevo Producto' para comenzar.")

    else:
        # VISTA DE FORMULARIO
        st.markdown("### 📝 Configuración de Producto")
        with st.form("form_producto_completo"):
            c1, c2, c3 = st.columns(3)
            sku = c1.text_input("SKU")
            nombre = c2.text_input("Nombre")
            cat = c3.selectbox("Categoría", ["Víveres", "Limpieza", "Hogar", "Otros"])
            
            st.markdown("#### 💰 Márgenes y Costos")
            m1, m2, m3 = st.columns(3)
            costo = m1.number_input("Costo Base", min_value=0.0)
            margen_detal = m2.number_input("Margen Detal (%)", 0.0)
            margen_mayor = m3.number_input("Margen Mayor (%)", 0.0)
            
            st.markdown("#### ⚖️ Impuestos y Comisiones")
            i1, i2 = st.columns(2)
            iva = i1.selectbox("IVA Aplicado", [0, 8, 16], format_func=lambda x: f"{x}%")
            comision = i2.number_input("Comisión Vendedor (%)", min_value=0.0, step=0.5)
            
            if st.form_submit_button("💾 Guardar en Inventario"):
                if not sku or not nombre:
                    st.error("⚠️ El SKU y el Nombre son campos obligatorios.")
                else:
                    datos = {'sku': sku, 'nom': nombre, 'cat': cat, 'costo': costo, 'mon': 'USD', 
                             'alm': 'Principal', 'md': margen_detal, 'mb': 0, 'mm': margen_mayor, 
                             'eb': 0, 'ed': 0, 'iva': iva, 'com': comision}
                    guardar_producto(datos)
                    st.session_state.modo_ingreso = False
                    st.rerun()

        if st.button("⬅️ Cancelar"):
            st.session_state.modo_ingreso = False
            st.rerun()
