import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(page_title="Calculadora de Pace", layout="centered")

st.title("🏃 Calculadora de Pace")
st.markdown("Descubra seu pace médio por quilômetro a partir da distância e tempo total.")

# Função para formatar entrada do tempo em tempo hh:mm:ss
def formatar_tempo_digitado(entrada):
    entrada = ''.join(filter(str.isdigit, entrada))[:6]
    entrada = entrada.zfill(6)
    horas = entrada[:2]
    minutos = entrada[2:4]
    segundos = entrada[4:6]
    return f"{horas}:{minutos}:{segundos}"

# Sessão de estado para tempo formatado
if "tempo_raw" not in st.session_state:
    st.session_state.tempo_raw = "0030"

# Input da distância
distancia = st.number_input("📏 Distância percorrida (km)", min_value=0.1, step=0.1, format="%.2f")

# Input com formatação dinâmica de tempo
tempo_digitado = st.text_input(
    "⏱️ Tempo total (digite como 0030 para 00:30)", 
    value=st.session_state.tempo_raw, 
    max_chars=6,
    key="tempo_input"
)

# Atualiza tempo formatado
tempo_formatado = formatar_tempo_digitado(tempo_digitado)
st.session_state.tempo_raw = tempo_digitado
st.caption(f"🧮 Interpretado como: `{tempo_formatado}`")

# Botão de cálculo
if st.button("✅ Calcular Pace"):
    try:
        h, m, s = map(int, tempo_formatado.split(":"))
        tempo_total_seg = h * 3600 + m * 60 + s

        if distancia == 0 or tempo_total_seg == 0:
            st.error("Distância e tempo devem ser maiores que zero.")
        else:
            pace_seg = tempo_total_seg / distancia
            pace_min = int(pace_seg // 60)
            pace_sec = int(pace_seg % 60)
            velocidade = (distancia / tempo_total_seg) * 3600

            st.success(f"🕒 **Pace:** {pace_min:02d}:{pace_sec:02d} min/km")
            st.success(f"🚴‍♂️ **Velocidade:** {velocidade:.1f} km/h")

            # Splits toggle
            if "mostrar_splits" not in st.session_state:
                st.session_state.mostrar_splits = False

            if st.button("👟 Ver/Ocultar Splits por KM"):
                st.session_state.mostrar_splits = not st.session_state.mostrar_splits

            if st.session_state.mostrar_splits:
                splits = []
                for km in range(1, int(distancia)+1):
                    tempo_km = int(pace_seg * km)
                    tempo_str = str(timedelta(seconds=tempo_km))
                    splits.append({
                        "KM": km,
                        "Tempo Acumulado": tempo_str,
                        "Velocidade (km/h)": f"{3600 / pace_seg:.1f}"
                    })
                st.markdown("### 📊 Splits por KM")
                st.dataframe(pd.DataFrame(splits), use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Conversor de pace
with st.expander("🧮 Converter Pace para Velocidade"):
    pace_convertido = st.text_input("Digite o pace (mm:ss)", value="06:00")
    try:
        min_pace, sec_pace = map(int, pace_convertido.split(":"))
        total_seg = min_pace * 60 + sec_pace
        velocidade_calc = 3600 / total_seg
        st.info(f"🚴 Velocidade correspondente: **{velocidade_calc:.2f} km/h**")
    except:
        st.warning("Digite no formato mm:ss, por exemplo: 05:30")
