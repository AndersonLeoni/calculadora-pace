import streamlit as st

st.set_page_config(page_title="Calculadora de Pace", layout="centered")

st.title("🏃 Calculadora de Pace (min/km)")
st.markdown("Informe o tempo total e a distância percorrida para calcular seu pace médio.")

col1, col2, col3 = st.columns(3)
with col1:
    horas = st.number_input("Horas", min_value=0, step=1, value=0)
with col2:
    minutos = st.number_input("Minutos", min_value=0, max_value=59, step=1, value=0)
with col3:
    segundos = st.number_input("Segundos", min_value=0, max_value=59, step=1, value=0)

distancia = st.number_input("Distância percorrida (em km)", min_value=0.1, step=0.1, value=5.0)

def calcular_pace(horas, minutos, segundos, distancia):
    tempo_total_segundos = horas * 3600 + minutos * 60 + segundos
    if distancia == 0:
        return None
    pace_seg = tempo_total_segundos / distancia
    pace_min = int(pace_seg // 60)
    pace_seg_restante = int(pace_seg % 60)
    return pace_min, pace_seg_restante

if st.button("Calcular Pace"):
    resultado = calcular_pace(horas, minutos, segundos, distancia)
    if resultado:
        st.success(f"🏁 Seu pace médio foi: **{resultado[0]}:{resultado[1]:02d} min/km**")
    else:
        st.error("Erro: a distância deve ser maior que zero.")
