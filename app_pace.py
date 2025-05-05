import streamlit as st
import re
from datetime import time

st.set_page_config(page_title="Calculadora de Pace", layout="centered")

st.title("🏃 Calculadora de Pace e Estratégia de Prova")

aba = st.radio("Escolha uma opção:", ["📏 Calcular Pace", "⚡ Converter Pace para km/h", "📊 Estratégia Pace Pro"], horizontal=True)


def pace_para_kmh(minutos, segundos):
    total_minutos = minutos + segundos / 60
    return round(60 / total_minutos, 2)


def tempo_input_personalizado(label):
    tempo_bruto = st.text_input(label, value="00:30:00", max_chars=8, help="Formato: hh:mm:ss")
    pattern = r"^(\d{1,2}):?(\d{1,2}):?(\d{1,2})$"
    match = re.match(pattern, tempo_bruto.replace(" ", ""))
    if match:
        h, m, s = [int(x) for x in match.groups()]
        return time(hour=h, minute=m, second=s)
    else:
        st.warning("Formato inválido. Use hh:mm:ss")
        return time(0, 0, 0)


if aba == "📏 Calcular Pace":
    distancia = st.number_input("Distância (km)", min_value=0.1, step=0.1)
    tempo = tempo_input_personalizado("Tempo total (hh:mm:ss)")

    if st.button("Calcular Pace"):
        total_minutos = tempo.hour * 60 + tempo.minute + tempo.second / 60
        pace = total_minutos / distancia
        minutos = int(pace)
        segundos = int((pace - minutos) * 60)
        pace_formatado = f"{minutos:02d}:{segundos:02d} min/km"
        km_h = round(60 / pace, 2)

        st.markdown(f"""
            ### Resultado
            - **Pace:** {pace_formatado}
            - **Velocidade:** {km_h} km/h
        """)

        if st.toggle("👟 Ver/ocultar parciais por km"):
            st.markdown("### 📏 Parciais por quilômetro")
            dados = []
            for km in range(1, int(distancia) + 1):
                tempo_km_min = pace * km
                min_km = int(tempo_km_min)
                seg_km = int((tempo_km_min - min_km) * 60)
                velocidade_km = round(60 / (tempo_km_min / km), 2)
                dados.append((f"{km} km", f"{min_km:02d}:{seg_km:02d}", f"{velocidade_km} km/h"))
            st.table(dados)

elif aba == "⚡ Converter Pace para km/h":
    minutos = st.number_input("Minutos por km", min_value=0, step=1)
    segundos = st.number_input("Segundos por km", min_value=0, max_value=59, step=1)

    if st.button("Converter"):
        km_h = pace_para_kmh(minutos, segundos)
        st.markdown(f"""
            ### Resultado
            - **Velocidade:** {km_h} km/h
        """)

elif aba == "📊 Estratégia Pace Pro":
    st.subheader("🎯 Planejamento Estratégico de Prova")

    distancia_total = st.number_input("Distância da prova (km)", min_value=1, step=1, key="dist_estrategia")
    tempo_prova = tempo_input_personalizado("Tempo estimado total (hh:mm:ss)")
    estrategia = st.selectbox("Estratégia de prova", ["Equilibrado", "Início mais leve", "Início mais forte"])

    total_minutos = tempo_prova.hour * 60 + tempo_prova.minute + tempo_prova.second / 60
    pace_medio = total_minutos / distancia_total

    variacao = 0.2  # 20% variação máxima no pace
    pace_por_km = []

    for km in range(1, int(distancia_total) + 1):
        if estrategia == "Equilibrado":
            pace_km = pace_medio
        elif estrategia == "Início mais leve":
            pace_km = pace_medio + variacao * ((int(distancia_total) - km) / int(distancia_total))
        elif estrategia == "Início mais forte":
            pace_km = pace_medio - variacao * (km / int(distancia_total))

        minutos = int(pace_km)
        segundos = int((pace_km - minutos) * 60)
        velocidade = round(60 / pace_km, 2)
        pace_por_km.append((f"{km} km", f"{minutos:02d}:{segundos:02d}", f"{velocidade} km/h"))

    st.markdown("### 📋 Estratégia por quilômetro")
    st.table(pace_por_km)
