import streamlit as st

st.set_page_config(page_title="Calculadora de Pace", layout="centered")
st.title("🏃 Calculadora de Pace e Velocidade")

aba = st.tabs(["📟 Calculadora", "🔁 Conversor"])

# ============================
# ABA 1: Calculadora de Pace
# ============================
with aba[0]:
    st.subheader("📟 Calcular Pace (min/km)")
    col1, col2, col3 = st.columns(3)
    with col1:
        horas = st.number_input("Horas", min_value=0, step=1, value=0)
    with col2:
        minutos = st.number_input("Minutos", min_value=0, max_value=59, step=1, value=0)
    with col3:
        segundos = st.number_input("Segundos", min_value=0, max_value=59, step=1, value=0)

    distancia = st.number_input("Distância (km)", min_value=0.1, step=0.1, value=5.0)

    def calcular_pace(horas, minutos, segundos, distancia):
        tempo_total_segundos = horas * 3600 + minutos * 60 + segundos
        if distancia == 0:
            return None
        pace_seg = tempo_total_segundos / distancia
        pace_min = int(pace_seg // 60)
        pace_seg_restante = int(pace_seg % 60)
        velocidade = round(3600 / pace_seg, 2)
        return pace_min, pace_seg_restante, velocidade

    if st.button("Calcular Pace"):
        resultado = calcular_pace(horas, minutos, segundos, distancia)
        if resultado:
            st.success(f"📊 Pace: **{resultado[0]}:{resultado[1]:02d} min/km**")
            st.info(f"🚀 Velocidade: **{resultado[2]} km/h**")
        else:
            st.error("Erro: a distância deve ser maior que zero.")

# ============================
# ABA 2: Conversor de Pace
# ============================
with aba[1]:
    st.subheader("🔁 Converter Pace para Velocidade (km/h)")
    col1, col2 = st.columns(2)
    with col1:
        pace_min = st.number_input("Minutos por km", min_value=0, value=7)
    with col2:
        pace_seg = st.number_input("Segundos por km", min_value=0, max_value=59, value=0)

    def pace_para_kmh(pace_min, pace_seg):
        tempo_total_min = pace_min + pace_seg / 60
        if tempo_total_min == 0:
            return None
        return round(60 / tempo_total_min, 2)

    if st.button("Converter Pace"):
        velocidade = pace_para_kmh(pace_min, pace_seg)
        if velocidade:
            st.success(f"🚀 Velocidade: **{velocidade} km/h**")
        else:
            st.error("Erro: o tempo deve ser maior que zero.")
