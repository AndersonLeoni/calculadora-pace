import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(page_title="Calculadora de Pace", layout="centered")

st.title("🏃 Calculadora de Pace")

# Função para formatar automaticamente tempo enquanto digita (dentro do input)
def formatar_tempo_input(valor):
    valor = ''.join(filter(str.isdigit, valor))[:6].zfill(6)
    return f"{valor[:2]}:{valor[2:4]}:{valor[4:]}"

# Sessão para armazenar estado do tempo bruto digitado
if "tempo_digitado" not in st.session_state:
    st.session_state.tempo_digitado = ""

# Distância
distancia = st.number_input("📏 Distância percorrida (km)", min_value=0.1, step=0.1, format="%.2f")

# Tempo com formatação dinâmica no próprio input
entrada_bruta = st.text_input("⏱️ Tempo total (hhmmss)", value=st.session_state.tempo_digitado, max_chars=6)
st.session_state.tempo_digitado = entrada_bruta
tempo_formatado = formatar_tempo_input(entrada_bruta)
st.caption(f"Tempo formatado: `{tempo_formatado}`")

if st.button("✅ Calcular Pace"):
    try:
        horas, minutos, segundos = map(int, tempo_formatado.split(":"))
        tempo_total_seg = horas * 3600 + minutos * 60 + segundos

        if tempo_total_seg == 0 or distancia == 0:
            st.error("Distância e tempo devem ser maiores que zero.")
        else:
            pace_seg = tempo_total_seg / distancia
            pace_min = int(pace_seg // 60)
            pace_sec = int(pace_seg % 60)
            velocidade = (distancia / tempo_total_seg) * 3600

            st.success(f"🕒 **Pace:** {pace_min:02d}:{pace_sec:02d} min/km")
            st.success(f"🚴‍♂️ **Velocidade média:** {velocidade:.1f} km/h")

            if "mostrar_splits" not in st.session_state:
                st.session_state.mostrar_splits = False

            if st.button("👟 Ver/Ocultar Splits por KM"):
                st.session_state.mostrar_splits = not st.session_state.mostrar_splits

            if st.session_state.mostrar_splits:
                splits = []
                for km in range(1, int(distancia) + 1):
                    tempo_km_seg = pace_seg * km
                    tempo_km_str = str(timedelta(seconds=int(tempo_km_seg)))
                    splits.append({
                        "KM": km,
                        "Tempo acumulado": tempo_km_str,
                        "Velocidade (km/h)": f"{3600 / pace_seg:.1f}"
                    })

                st.markdown("### 📊 Splits por KM")
                st.table(pd.DataFrame(splits))

    except Exception as e:
        st.error(f"Erro ao calcular pace: {e}")

with st.expander("🧮 Conversor de Pace para Velocidade"):
    pace_convertido = st.text_input("Digite o pace (mm:ss)", value="06:00")
    try:
        min_pace, sec_pace = map(int, pace_convertido.split(":"))
        total_seg = min_pace * 60 + sec_pace
        velocidade_calc = 3600 / total_seg
        st.info(f"🚴 Velocidade correspondente: **{velocidade_calc:.2f} km/h**")
    except:
        st.warning("Digite no formato mm:ss, por exemplo: 05:30")
