import streamlit as io_streamlit
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Configuración de página de Streamlit
io_streamlit.set_page_config(page_title="Dashboard Inteligente Multi-Moneda", layout="wide", page_icon="📊")

def verificar_y_crear_datos_simulados():
    """Detecta si la base de datos existe. Si no, la crea e inyecta la estructura y 10 ventas de prueba."""
    conn = sqlite3.connect('inventario_inteligente_v3.db')
    cursor = conn.cursor()
    
    # 1. Crear estructuras básicas si no existen
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (username TEXT, password TEXT, rol TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (cedula_rif TEXT PRIMARY KEY, nombre TEXT, telefono TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (codigo TEXT PRIMARY KEY, descripcion TEXT, precio_detal_usd REAL, precio_bulto_usd REAL, precio_mayor_usd REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ventas (id INTEGER PRIMARY KEY, fecha TEXT, vendedor TEXT, cliente_id TEXT, codigo_producto TEXT, cantidad INTEGER, precio_final_usd REAL)''')
    
    # 2. Verificar si está vacía para inyectar la simulación comercial
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        # Inyección de Productos (Extraídos de tu lista base)
        productos = [
            ('SUPE0003', 'BIANCHI CARAMELO CHOCOLATE 18BX100U', 48.88, 43.24, 41.00),
            ('SUPE0010', 'TRULULU AROS 36BX50U', 75.00, 68.50, 65.00),
            ('SUPE0013', 'LOKIÑO CARAMELO 24BX100U', 55.50, 50.00, 47.50)
        ]
        cursor.executemany("INSERT INTO productos VALUES (?, ?, ?, ?, ?)", productos)
        
        # Inyección de Clientes de prueba (Venezuela)
        clientes = [
            ('V-12345678', 'Distribuidora Central, C.A.', '584121234567'),
            ('V-87654321', 'Comercial El Surtido', '584149876543'),
            ('J-99999999', 'Inversiones Confite Caracas', '584241112233')
        ]
        cursor.executemany("INSERT INTO clientes VALUES (?, ?, ?)", clientes)
        
        # Generación Automática de 10 Ventas falsas realistas para no dejar vacío el Excel
        vendedores = ['cajero1', 'cajero2', 'super']
        hoy = datetime.now()
        
        for i in range(10):
            prod_elegido = random.choice(productos)
            cli_elegido = random.choice(clientes)
            vend_elegido = random.choice(vendedores)
            
            # Variación de precios según tipo de venta simulada (Detal, Bulto o Mayor)
            precio_aplicado = random.choice([prod_elegido[2], prod_elegido[3], prod_elegido[4]])
            cantidad = random.randint(2, 15)
            total_venta = precio_aplicado * cantidad
            fecha_venta = (hoy - timedelta(hours=random.randint(1, 8))).strftime('%Y-%m-%d %H:%M')
            
            cursor.execute('''INSERT INTO ventas (fecha, vendedor, cliente_id, codigo_producto, cantidad, precio_final_usd) 
                              VALUES (?, ?, ?, ?, ?, ?)''', (fecha_venta, vend_elegido, cli_elegido[0], prod_elegido[0], cantidad, total_venta))
            
    conn.commit()
    conn.close()

def generar_buffer_excel(df_reporte):
    """Genera el archivo de Excel en memoria para que pueda descargarse desde la web."""
    wb = Workbook()
    ws = wb.active
    ws.title = "📊 Control Gerencial de Ventas"
    ws.views.sheetView.showGridLines = True

    font_titulo = Font(name="Segoe UI", size=15, bold=True, color="FFFFFF")
    font_cabecera = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    font_datos = Font(name="Segoe UI", size=10)
    font_totales = Font(name="Segoe UI", size=11, bold=True)
    
    fill_titulo = PatternFill(start_color="1B4F72", end_color="1B4F72", fill_type="solid")
    fill_cabecera = PatternFill(start_color="2E4053", end_color="2E4053", fill_type="solid")
    fill_totales = PatternFill(start_color="F2F4F4", end_color="F2F4F4", fill_type="solid")

    border_fino = Border(
        left=Side(style='thin', color='D5D8DC'), right=Side(style='thin', color='D5D8DC'),
        top=Side(style='thin', color='D5D8DC'), bottom=Side(style='thin', color='D5D8DC')
    )

    ws.merge_cells("A1:G1")
    ws["A1"] = "MONITOR DE OPERACIONES Y RENDIMIENTO COMERCIAL"
    ws["A1"].font = font_titulo
    ws["A1"].fill = fill_titulo
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions.height = 35

    headers = ["Fecha / Hora", "Vendedor", "Cliente ID", "SKU Producto", "Cantidad", "Total Facturado (USD)", "Utilidad Neta (USD)"]
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_num)
        cell.value = header
        cell.font = font_cabecera
        cell.fill = fill_cabecera
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions.height = 25

    row_num = 4
    for index, row in df_reporte.iterrows():
        ws.cell(row=row_num, column=1, value=str(row['fecha'])).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=2, value=str(row['vendedor'])).alignment = Alignment(horizontal="left")
        ws.cell(row=row_num, column=3, value=str(row['cliente_id'])).alignment = Alignment(horizontal="center")
        ws.cell(row=row_num, column=4, value=str(row['codigo_producto'])).alignment = Alignment(horizontal="center")
        
        cant_cell = ws.cell(row=row_num, column=5, value=int(row['cantidad']))
        cant_cell.number_format = '#,##0'
        cant_cell.alignment = Alignment(horizontal="right")
        
        cobrado_cell = ws.cell(row=row_num, column=6, value=float(row['precio_final_usd']))
        cobrado_cell.number_format = '$#,##0.00'
        cobrado_cell.alignment = Alignment(horizontal="right")
        
        utilidad_cell = ws.cell(row=row_num, column=7, value=float(row['utilidad_neta_usd']))
        utilidad_cell.number_format = '$#,##0.00'
        utilidad_cell.alignment = Alignment(horizontal="right")

        for col_num in range(1, 8):
            c = ws.cell(row=row_num, column=col_num)
            c.font = font_datos
            c.border = border_fino
        row_num += 1

    ws.cell(row=row_num, column=4, value="TOTALES:").font = font_totales
    ws.cell(row=row_num, column=4).alignment = Alignment(horizontal="right")
    
    ws.cell(row=row_num, column=5, value=f"=SUM(E4:E{row_num-1})").number_format = '#,##0'
    ws.cell(row=row_num, column=6, value=f"=SUM(F4:F{row_num-1})").number_format = '$#,##0.00'
    ws.cell(row=row_num, column=7, value=f"=SUM(G4:G{row_num-1})").number_format = '$#,##0.00'

    for col_num in range(1, 8):
        c = ws.cell(row=row_num, column=col_num)
        c.font = font_totales
        c.fill = fill_totales
        c.border = border_fino
        if col_num >= 5:
            c.alignment = Alignment(horizontal="right")

    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col.column)
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer

# --- FLUJO DE LA APLICACIÓN WEB STREAMLIT ---
io_streamlit.title("📊 Ecosistema Comercial Inteligente")
io_streamlit.subheader("Control Gerencial de Ventas e Inventario para Venezuela")

# Inicialización segura de la data de confitería
verificar_y_crear_datos_simulados()

conn = sqlite3.connect('inventario_inteligente_v3.db')
df_ventas = pd.read_sql_query("SELECT * FROM ventas", conn)
df_productos = pd.read_sql_query("SELECT * FROM productos", conn)
conn.close()

# Procesamiento de márgenes comerciales
df_reporte = df_ventas.merge(df_productos, left_on='codigo_producto', right_on='codigo', how='left')
df_reporte['costo_base_usd'] = df_reporte['precio_mayor_usd'] * 0.75
df_reporte['costo_total_usd'] = df_reporte['cantidad'] * df_reporte['costo_base_usd']
df_reporte['utilidad_neta_usd'] = df_reporte['precio_final_usd'] - df_reporte['costo_total_usd']

# Tarjetas KPI Dinámicas en el Navegador Web
col1, col2, col3 = io_streamlit.columns(3)
with col1:
    io_streamlit.metric(label="📦 Volumen de Ventas (Unidades)", value=f"{int(df_reporte['cantidad'].sum()):,}")
with col2:
    io_streamlit.metric(label="💵 Total Facturado Bruto", value=f"${df_reporte['precio_final_usd'].sum():,.2f} USD")
with col3:
    io_streamlit.metric(label="📈 Utilidad Neta Real", value=f"${df_reporte['utilidad_neta_usd'].sum():,.2f} USD")

io_streamlit.write("---")

# Tabla Interactiva en vivo (Editable y filtrable desde el navegador)
io_streamlit.write("### 📝 Registro Histórico de Operaciones del Turno")
io_streamlit.dataframe(df_reporte[['fecha', 'vendedor', 'cliente_id', 'codigo_producto', 'cantidad', 'precio_final_usd', 'utilidad_neta_usd']], use_container_width=True)

io_streamlit.write("---")

# Botón de Descarga Digital Inteligente para Excel
io_streamlit.write("### 📥 Descarga de Auditoría Contable")
excel_file = generar_buffer_excel(df_reporte)

io_streamlit.download_button(
    label="🟢 Descargar Reporte Formateado en Excel",
    data=excel_file,
    file_name="Reporte_Gerencial_Ecosistema.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
