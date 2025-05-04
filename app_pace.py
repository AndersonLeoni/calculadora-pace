import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(page_title="Calculadora de Pace", layout="centered")

st.title("🏃 Calculadora de Pace")
st.markdown("Descubra seu pace médio por quilômetro a partir da distância e tempo total.")

# Função para formatar tempo inserido (ex: 123 -> 00:01:23 ou 930 -> 00:09:30)
def formatar_tempo(entrada):
    entrada = ''.join(filter(str.isdigit, entrada))[:6]  # Limita a 6 dígitos
    entrada = entrada.zfill(6)
    horas = entrada[:2]
    minutos = entrada[2:4]
    segundos = entrada[4:6]
    return f"{horas}:{minutos}:{segundos}"

# Entradas
col1, col2 = st.columns(2)
with col1:
    distancia = st.number_input("Distância percorrida (km)", min_value=0.1, step=0.1, format="%.2f")

with col2:
    tempo_input = st.text_input("Tempo total (hhmmss)", value="0030")
    tempo_formatado = formatar_tempo(tempo_input)
    st.text(f"Tempo formatado: {tempo_formatado}")

# Calcular pace
if st.button("✅ Calcular Pace"):
    h, m, s = map(int, tempo_formatado.split(":"))
    tempo_total_seg = h * 3600 + m * 60 + s

    if distancia == 0:
        st.error("Distância deve ser maior que zero.")
    elif tempo_total_seg == 0:
        st.error("Tempo total deve ser maior que zero.")
    else:
        pace_seg = tempo_total_seg / distancia
        pace_min = int(pace_seg // 60)
        pace_sec = int(pace_seg % 60)
        velocidade = (distancia / tempo_total_seg) * 3600

        st.success(f"🕒 **Pace:** {pace_min:02d}:{pace_sec:02d} min/km")
        st.success(f"🚴‍♂️ **Velocidade:** {velocidade:.1f} km/h")

        # Exibir/ocultar parciais
        if 'mostrar_parciais' not in st.session_state:
            st.session_state.mostrar_parciais = False

        if st.button("👟 Ver/Ocultar Parciais por KM"):
            st.session_state.mostrar_parciais = not st.session_state.mostrar_parciais

        if st.session_state.mostrar_parciais:
            # Gerar splits
            splits = []
            for km in range(1, int(distancia)+1):
                parcial_seg = pace_seg * km
                parcial_tempo = str(timedelta(seconds=int(parcial_seg)))
                vel_km = 3600 / pace_seg
                splits.append({"KM": km, "Tempo Parcial": parcial_tempo, "Velocidade (km/h)": f"{vel_km:.1f}"})

            df = pd.DataFrame(splits)
            st.markdown("### 📊 Splits por KM")
            st.dataframe(df, use_container_width=True)

# Conversor de Pace
with st.expander("🧮 Converter Pace para Velocidade"):
    pace_convertido = st.text_input("Digite o pace (min/km)", value="06:00")
    try:
        min_pace, sec_pace = map(int, pace_convertido.split(":"))
        total_seg = min_pace * 60 + sec_pace
        velocidade_calc = 3600 / total_seg
        st.info(f"🚴 Velocidade correspondente: **{velocidade_calc:.2f} km/h**")
    except:
        st.warning("Digite no formato mm:ss, por exemplo: 05:30")
