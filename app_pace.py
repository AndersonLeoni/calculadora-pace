import streamlit as st
from datetime import time

# Estilo CSS
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
        margin-top: 10px;
    }

    .parcial {
        background-color: #f0f0f0;
        padding: 8px 15px;
        border-radius: 8px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="titulo-principal">Calculadora de Pace</div>', unsafe_allow_html=True)
st.markdown('<div class="descricao">Descubra seu pace médio por quilômetro a partir da distância e tempo total.</div>', unsafe_allow_html=True)

# Estados iniciais
if "resultado_exibido" not in st.session_state:
    st.session_state.resultado_exibido = False

if "mostrar_parciais" not in st.session_state:
    st.session_state.mostrar_parciais = False

# Entradas (agora em linha única)
distancia = st.number_input("📏 Distância percorrida (km)", min_value=0.0, step=0.1, format="%.2f")
tempo = st.time_input("⏳ Tempo total (hh:mm:ss)", value=time(0, 0, 0))

# Botão calcular
if st.button("Calcular Pace"):
    if distancia == 0:
        st.warning("Por favor, insira uma distância maior que zero.")
        st.session_state.resultado_exibido = False
    else:
        total_minutos = tempo.hour * 60 + tempo.minute + tempo.second / 60
        pace = total_minutos / distancia
        minutos = int(pace)
        segundos = int((pace - minutos) * 60)
        st.session_state.pace_formatado = f"{minutos:02d}:{segundos:02d} min/km"
        st.session_state.km_h = round(60 / pace, 2)
        st.session_state.pace_valor = pace
        st.session_state.distancia = distancia
        st.session_state.resultado_exibido = True

# Resultado principal
if st.session_state.resultado_exibido:
    st.markdown(f'''
        <div class="resultado">
            ⏱️ <strong>Pace:</strong> {st.session_state.pace_formatado} <br>
            🚀 <strong>Velocidade:</strong> {st.session_state.km_h} km/h
        </div>
    ''', unsafe_allow_html=True)

    # Botão de parciais
    if st.button("👟 Ver/Ocultar Parciais por KM"):
        st.session_state.mostrar_parciais = not st.session_state.mostrar_parciais

    # Parciais
    if st.session_state.mostrar_parciais:
        st.markdown("### 📊 Parciais por Quilômetro")
        for km in range(1, int(st.session_state.distancia) + 1):
            tempo_km_min = st.session_state.pace_valor * km
            min_km = int(tempo_km_min)
            seg_km = int((tempo_km_min - min_km) * 60)
            vel_km = round(60 / (tempo_km_min / km), 2)  # velocidade parcial
            st.markdown(f'<div class="parcial">KM {km:02d}: ⏱️ {min_km:02d}:{seg_km:02d} | 🚀 {vel_km} km/h</div>', unsafe_allow_html=True)
