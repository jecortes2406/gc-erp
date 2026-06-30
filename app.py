from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Custom Cloud ERP - Núcleo Modular",
    description="API Base para ERP en la nube 100% modificable y adaptable",
    version="1.0.0"
)

# --- MODELOS DE DATOS (Modificables) ---
class Producto(BaseModel):
    id: int
    nombre: str
    codigo_sku: str
    precio_usd: float
    stock_actual: int

class TransaccionFactura(BaseModel):
    cliente_rif: str
    monto_usd: float
    metodo_pago: str  # Ejemplo: "Efectivo USD", "Transferencia VES", "Pago Movil"
    tasa_bcv: float

# --- BASE DE DATOS SIMULADA EN MEMORIA ---
# Puedes conectar esto a PostgreSQL, MySQL o MongoDB fácilmente
inventario_db: List[Producto] = [
    {"id": 1, "nombre": "Materia Prima Tipo A", "codigo_sku": "MP-001", "precio_usd": 10.50, "stock_actual": 150}
]

# --- RUTAS Y FUNCIONES LOGICAS ---

@app.get("/", tags=["General"])
def inicio():
    return {"status": "Online", "sistema": "ERP Cloud Personalizado v1"}

@app.get("/inventario", response_model=List[Producto], tags=["Inventario"])
def obtener_inventario():
    """Devuelve todos los productos del inventario en tiempo real"""
    return inventario_db

@app.post("/inventario/agregar", tags=["Inventario"])
def agregar_producto(producto: Producto):
    """Función para añadir nuevos productos al stock"""
    inventario_db.append(producto.dict())
    return {"message": "Producto registrado exitosamente", "producto": producto}

@app.post("/facturacion/procesar", tags=["Finanzas y Fiscalidad"])
def procesar_factura(factura: TransaccionFactura):
    """
    Bloque Lógico Fiscal Modificable:
    Calcula montos, conversión a moneda local y aplica impuestos automáticamente (Ej: IGTF 3%).
    """
    monto_bolivares = factura.monto_usd * factura.tasa_bcv
    igtf_aplicado = 0.0
    total_final_usd = factura.monto_usd

    # Lógica modificable: Si paga en divisas en efectivo, se calcula el IGTF
    if factura.metodo_pago == "Efectivo USD":
        igtf_aplicado = factura.monto_usd * 0.03
        total_final_usd = factura.monto_usd + igtf_aplicado
    
    total_final_ves = total_final_usd * factura.tasa_bcv

    return {
        "status": "Procesada",
        "cliente_rif": factura.cliente_rif,
        "monto_base_usd": factura.monto_usd,
        "monto_base_ves": monto_bolivares,
        "igtf_3_porciento_usd": igtf_aplicado,
        "total_a_pagar_usd": total_final_usd,
        "total_a_pagar_ves": total_final_ves,
        "mensaje_fiscal": "Listo para envío a firma digital o impresora homologada."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
