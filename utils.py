# --- MOTOR DE TASAS CENTRALIZADO ---
@st.cache_data(ttl=3600) # Se actualiza automáticamente cada hora
def obtener_tasas():
    # En un entorno real, aquí podrías conectar con una API (ej. dispotech)
    # Por ahora, definimos los valores base para tu control manual
    return 46.50, 765.00 # USD_Binance, USD_BCV

# Inicializamos las tasas en el session_state si no existen
if 'tasa_binance' not in st.session_state:
    st.session_state.tasa_binance, st.session_state.tasa_bcv = obtener_tasas()

# Panel de Control de Tasas en la Barra Lateral
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Control de Tasas (Master)")
st.session_state.tasa_binance = st.sidebar.number_input("Tasa Binance (P2P)", value=st.session_state.tasa_binance, format="%.2f")
st.session_state.tasa_bcv = st.sidebar.number_input("Tasa BCV", value=st.session_state.tasa_bcv, format="%.2f")

# Definimos cuál usaremos como "Master" para cálculos
st.session_state.referencia_master = st.session_state.tasa_binance
st.sidebar.info(f"Referencia de Carga: {st.session_state.referencia_master} Bs/USD")
