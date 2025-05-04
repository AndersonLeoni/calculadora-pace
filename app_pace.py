import streamlit as st
import pandas as pd
from datetime import time

# --- Estilos personalizados ---
st.markdown("""
<style>
    .titulo {
        text-align: center;
        font-size: 2em;
        font-weight: bold;
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
</style>
""", unsafe_allow_html=True)

# --- Título e descrição ---
st.markdown('<div class="titulo">Calculadora de Pace</div>', unsafe_allow_html=True)
st.markdown('<div class="descricao">Descubra seu pace médio por quilômetro a partir da distância e tempo total.</div>', unsafe_allow_html=True)

# --- Tabs ---
aba = st.tabs(["🏃‍♂️ Calcular Pace", "🔁 Conversão de Pace"])[0]

with st.container():
    # --- Estados globais ---
    if "mostrar_parciais" not in st.session_state:
        st.session_state.mostrar_parciais = False

    # --- Entradas do usuário ---
    distancia = st.number_input("📏 Distância percorrida (km)", min_value=0.0, step=0.1, format="%.2f")
    tempo = st.time_input("⏳ Tempo total (hh:mm:ss)", value=time(0, 30, 0))

    if st.button("Calcular Pace"):
        if distancia == 0:
            st.warning("Por favor, insira uma distância maior que zero.")
        else:
            total_min = tempo.hour * 60 + tempo.minute + tempo.second / 60
            pace = total_min / distancia
            minutos = int(pace)
            segundos = int((pace - minutos) * 60)
            pace_formatado = f"{minutos:02d}:{segundos:02d} min/km"
            velocidade = round(60 / pace, 2)

            # --- Mostrar resultados ---
            st.markdown(f'''
                <div class="resultado">
                    ⏱️ <strong>Pace:</strong> {pace_formatado} <br>
                    🚀 <strong>Velocidade:</strong> {velocidade} km/h
                </div>
            ''', unsafe_allow_html=True)

            # --- Botão de parciais ---
            if st.button("👟 Ver/Ocultar Parciais por KM"):
                st.session_state.mostrar_parciais = not st.session_state.mostrar_parciais

            # --- Exibir tabela com splits ---
            if st.session_state.mostrar_parciais:
                st.markdown("### 📊 Tabela de Splits por KM")

                data = []
                for km in range(1, int(distancia) + 1):
                    parcial_min = pace * km
                    min_parcial = int(parcial_min)
                    seg_parcial = int((parcial_min - min_parcial) * 60)
                    vel_km = round(60 / (parcial_min / km), 2)
                    data.append({
                        "KM": km,
                        "Tempo Parcial": f"{min_parcial:02d}:{seg_parcial:02d}",
                        "Velocidade (km/h)": vel_km
                    })

                df_parciais = pd.DataFrame(data)
                st.dataframe(df_parciais, use_container_width=True)

# --- Aba de Conversão de Pace ---
with st.tabs(["🏃‍♂️ Calcular Pace", "🔁 Conversão de Pace"])[1]:
    st.markdown("### 🎯 Conversão de Pace para Velocidade")

    pace_min = st.number_input("Minutos por KM", min_value=0, max_value=59, step=1)
    pace_sec = st.number_input("Segundos por KM", min_value=0, max_value=59, step=1)

    if st.button("Converter Pace para km/h"):
        total_min = pace_min + pace_sec / 60
        if total_min == 0:
            st.warning("O pace não pode ser zero.")
        else:
            velocidade = round(60 / total_min, 2)
            st.success(f"🚀 Velocidade equivalente: {velocidade} km/h")
