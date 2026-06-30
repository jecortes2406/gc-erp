import sqlite3
import pandas as pd
import plotly.subplots as sp
import plotly.express as px
from datetime import datetime
import os

def inicializar_db():
    conn = sqlite3.connect('gc_sistema.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, quiosco TEXT, subtotal REAL, iva REAL, total_usd REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, concepto TEXT, monto REAL)''')
    conn.commit()
    conn.close()

def registrar_movimiento(tipo):
    conn = sqlite3.connect('gc_sistema.db')
    cursor = conn.cursor()
    if tipo == 'venta':
        quiosco = input("Nombre del Quiosco: ")
        sub = float(input("…
import streamlit as st
import pandas as pd
import sqlite3
import plotly.subplots as sp
import plotly.express as px
from datetime import datetime

# Configuración de página profesional
st.set_page_config(layout="wide", page_title="GC Grupo Comercial ERP")

# Inicialización de Base de Datos
def init_db():
    conn = sqlite3.connect('gc_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ventas 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, quiosco TEXT, subtotal REAL, iva REAL, total_usd REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS gastos 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, concepto TEXT, monto REAL)''')
    conn.commit()
    conn.close()

init_db()

# Interfaz Principal
st.title("🌐 GC GRUPO COMERCIAL - ERP Cloud Base")
menu = st.sidebar.selectbox("Módulos de Gestión", ["Registrar Venta", "Registrar Gasto", "Dashboard Maestro"])

if menu == "Registrar Venta":
    st.subheader("Módulo de Ventas")
    q = st.text_input("Nombre del Quiosco")
    sub = st.number_input("Monto Base (Subtotal)")
    if st.button("Registrar Venta"):
        iva = sub * 0.16
        tot = sub + iva
        conn = sqlite3.connect('gc_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO ventas (fecha, quiosco, subtotal, iva, total_usd) VALUES (?,?,?,?,?)", 
                  (datetime.now().strftime('%Y-%m-%d'), q, sub, iva, tot))
        conn.commit()
        conn.close()
        st.success(f"Venta registrada: {tot} USD (IVA incluido).")

elif menu == "Registrar Gasto":
    st.subheader("Módulo de Gastos")
    concep = st.text_input("Concepto del Gasto")
    monto = st.number_input("Monto del Gasto")
    if st.button("Registrar Gasto"):
        conn = sqlite3.connect('gc_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO gastos (fecha, concepto, monto) VALUES (?,?,?)", 
                  (datetime.now().strftime('%Y-%m-%d'), concep, monto))
        conn.commit()
        conn.close()
        st.success("Gasto registrado con éxito.")

elif menu == "Dashboard Maestro":
    st.subheader("Centro de Control Financiero")
    conn = sqlite3.connect('gc_data.db')
    df_v = pd.read_sql_query("SELECT * FROM ventas", conn)
    df_g = pd.read_sql_query("SELECT * FROM gastos", conn)
    conn.close()
    
    if not df_v.empty:
        fig = sp.make_subplots(
            rows=2, cols=2,
            subplot_titles=("Ventas por Quiosco", "Tendencia", "Distribución", "Balance (Ventas vs Gastos)"),
            specs=[[{"type": "xy"}, {"type": "xy"}], [{"type": "domain"}, {"type": "xy"}]]
        )
        
        fig.add_trace(px.bar(df_v, x='quiosco', y='total_usd').data[0], row=1, col=1)
        fig.add_trace(px.line(df_v, x='fecha', y='total_usd').data[0], row=1, col=2)
        fig.add_trace(px.pie(df_v, names='quiosco', values='total_usd').data[0], row=2, col=1)
        
        if not df_g.empty:
            fig.add_trace(px.bar(x=['Ingresos', 'Egresos'], y=[df_v['total_usd'].sum(), df_g['monto'].sum()], color=['green', 'red']).data[0], row=2, col=2)
        
        fig.update_layout(height=700, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos suficientes para mostrar el Dashboard.")
