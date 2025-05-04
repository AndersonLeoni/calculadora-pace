import streamlit as st
from datetime import time

# Estilo CSS personalizado
st.markdown("""
<style>
    .titulo-principal {
        font-size: 2.2em;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
    }

    .descricao {
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 20px;
    }

    .resultado {
        background-color: #2e7d32;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 1.3em;
        text-align: center;
    }

    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# Título e descrição
st.markdown('<div class="titulo-principal">Calculadora de Pace</div>', unsafe_allow_html=True)
st.markdown('<div class="descricao">Descubra seu pace médio por quilômetro a partir da distância e tempo total.</div>', unsafe_allow_html=True)

# Inicializar variáveis de estado se não existirem
if 'pace_calculado' not in st.session_state:
    st.session_state.pace_calculado = False
if 'mostrar_parciais' not in st.session_state:
    st.session_state.mostrar_parciais = False

# Entradas do usuário
col1, col2 = st.columns(2)
with col1:
    distancia = st.number_input("Distância percorrida (km)", min_value=0.0, step=0.1, format="%.2f")
with col2:
    tempo = st.time_input("Tempo total (hh:mm:ss)", value=time(0, 0, 0))

# Botão de calcular
if st.button("Calcular Pace"):
    if distancia == 0:
        st.warning("Por favor, insira uma distância maior que zero.")
        st.session_state.pace_calculado = False
    else:
        total_minutos = tempo.hour * 60 + tempo.minute + tempo.second / 60
        pace = total_minutos / distancia
        minutos = int(pace)
        segundos = int((pace - minutos) * 60)
        st.session_state.pace_formatado = f"{minutos:02d}:{segundos:02d} min/km"
        st.session_state.km_h = round(60 / pace, 2)
        st.session_state.pace_valor = pace
        st.session_state.distancia = distancia
        st.session_state.pace_calculado = True

# Exibir resultado se pace foi calculado
if st.session_state.pace_calculado:
    st.markdown(f'''
        <div class="resultado">
            <div style="display: flex; align-items: center; gap: 10px; justify-content: center;">
                <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
                    <path d="M12 8a1 1 0 0 1 1 1v3.586l1.707 1.707a1 1 0 0 1-1.414 1.414l-2-2A1 1 0 0 1 11 13V9a1 1 0 0 1 1-1z"/>
                    <path fill-rule="evenodd" d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/>
                </svg>
                <strong>Pace:</strong> {st.session_state.pace_formatado}
            </div>
            <div style="display: flex; align-items: center; gap: 10px; justify-content: center; margin-top: 10px;">
                <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
                    <path d="M13 3a1 1 0 0 1 1 1v3.055a7.001 7.001 0 0 1 5.44 8.385 1 1 0 0 1-1.944-.43A5.002 5.002 0 0 0 14 8.127V12a1 1 0 0 1-2 0V4a1 1 0 0 1 1-1z"/>
                    <path d="M6 20a1 1 0 0 1-1-1c0-2.761 4.03-5 9-5s9 2.239 9 5a1 1 0 0 1-1 1H6z"/>
                </svg>
                <strong>Velocidade:</strong> {st.session_state.km_h} km/h
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Toggle para mostrar/ocultar parciais
    st.session_state.mostrar_parciais = st.toggle("👟 Ver/ocultar parciais por km", value=st.session_state.mostrar_parciais)

    if st.session_state.mostrar_parciais:
        st.markdown("### 📏 Parciais por quilômetro")
        for km in range(1, int(st.session_state.distancia) + 1):
            tempo_km_min = st.session_state.pace_valor * km
            min_km = int(tempo_km_min)
            seg_km = int((tempo_km_min - min_km) * 60)
            st.write(f"KM {km:02d}: {min_km:02d}:{seg_km:02d}")
