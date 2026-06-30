import streamlit as st

def mostrar_formulario_inventario():
    st.title("PROBANDO MÓDULO")
    st.write("Si ves este mensaje, la conexión está perfecta.")
    
    # Esto garantiza que siempre se vea algo
    if st.button("Botón de prueba"):
        st.success("¡El botón funciona!")
