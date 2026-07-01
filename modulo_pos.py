
    
    # 1. Obtenemos inventario
    data = obtener_todos_productos()
    if not data:
        st.warning("No hay productos en inventario.")
        return
    
    df = pd.DataFrame(data, columns=["ID", "Nombre", "SKU", "Costo", "P.Base", "Precio_Venta_Bs", "Stock"])
    
    # 2. Selección de producto
    seleccion = st.selectbox("Seleccionar Producto", df['Nombre'].tolist())
    producto = df[df['Nombre'] == seleccion].iloc[0]
    
    st.write(f"*Precio:* Bs. {producto['Precio_Venta_Bs']:.2f} | *Stock disponible:* {producto['Stock']}")
    
    cantidad = st.number_input("Cantidad", min_value=1, max_value=int(producto['Stock']))
    
    if st.button("✅ PROCESAR VENTA"):
        if cantidad <= producto['Stock']:
            actualizar_stock(producto['ID'], cantidad)
            st.success(f"Venta de {cantidad} {producto['Nombre']} realizada con éxito.")
            st.rerun() # Recargamos para ver stock actualizado
        else:
            st.error("Stock insuficiente.")
