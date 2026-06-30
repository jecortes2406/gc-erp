import sqlite3
import streamlit as st

# Inicialización de la base de datos profesional
def init_db():
    conn = sqlite3.connect('sistema_gc.db')
    c = conn.cursor()
    # Tabla de Productos con lógica de comisiones escalonadas
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    costo_original REAL,
                    moneda_adquisicion TEXT,
                    tasa_hist REAL,
                    margen_detal REAL,
                    margen_bulto REAL,
                    margen_mayor REAL,
                    pct_comision_detal REAL,
                    pct_comision_bulto REAL,
                    pct_comision_mayor REAL
                )''')
    conn.commit()
    conn.close()

# Función para añadir producto (se usará en el formulario de inventario)
def agregar_producto(datos):
    conn = sqlite3.connect('sistema_gc.db')
    c = conn.cursor()
    c.execute('''INSERT INTO productos (nombre, costo_original, moneda_adquisicion, tasa_hist, 
                 margen_detal, margen_bulto, margen_mayor, 
                 pct_comision_detal, pct_comision_bulto, pct_comision_mayor) 
                 VALUES (?,?,?,?,?,?,?,?,?,?)''', datos)
    conn.commit()
    conn.close()

# Inicializamos al arrancar la app
init_db()
