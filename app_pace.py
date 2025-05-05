import streamlit as st
from datetime import time

st.set_page_config(page_title="Calculadora de Pace", layout="centered")

st.markdown("""
    <style>
        .resultado {
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 12px;
            margin-top: 1rem;
            font-size: 1.3rem;
            text-align: center;
        }
        .split-table {
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏃 Calculadora de Pace e Estratégia de Prova")

aba = st.radio("Escolha uma opção:", ["📏 Calcular Pace", "⚡ Converter Pace", "🧠 Estratégia Pace Pro"], horizontal=True)

def calcular_splits(distancia, pace_min_km):
    dados = []
    for km in range(1, int(distancia) + 1):
        total_min = pace_min_km * km
        minutos = int(pace_min_km)
        segundos = int((pace_min_km - minutos) * 60)
        velocidade = round(60 / pace_min_km, 2)
        dados.append((str(km), f"{minutos:02d}:{segundos:02d}", f"{velocidade} km/h"))
    return dados

def mostrar_tabela_splits(dados, titulo):
    st.markdown(f"### {titulo}")
    st.table({
        "KM": [d[0] for d in dados],
        "Pace": [d[1] for d in dados],
        "Velocidade": [d[2] for d in dados]
    })

if aba == "📏 Calcular Pace":
    st.subheader("📏 Calcular Pace")
    distancia = st.number_input("Distância (km)", min_value=0.1, step=0.1)
    tempo = st.time_input("Tempo total (hh:mm:ss)", value=time(0, 30, 0))

    if "pace_calculado" not in st.session_state:
        st.session_state.pace_calculado = False

    if st.button("Calcular Pace"):
        total_minutos = tempo.hour * 60 + tempo.minute + tempo.second / 60
        pace_min_km = total_minutos / distancia
        minutos = int(pace_min_km)
        segundos = int((pace_min_km - minutos) * 60)
        velocidade = round(60 / pace_min_km, 2)

        st.session_state.resultado = {
            "pace": f"{minutos:02d}:{segundos:02d}",
            "velocidade": velocidade,
            "splits": calcular_splits(distancia, pace_min_km)
        }
        st.session_state.pace_calculado = True

    if st.session_state.pace_calculado:
        resultado = st.session_state.resultado
        st.markdown(f"""
            <div class="resultado">
                <strong>⏱️ Pace:</strong> {resultado["pace"]} min/km<br>
                <strong>🚀 Velocidade:</strong> {resultado["velocidade"]} km/h
            </div>
        """, unsafe_allow_html=True)

        exibir_splits = st.toggle("👟 Ver splits por km", value=False)
        if exibir_splits:
            mostrar_tabela_splits(st.session_state.resultado["splits"], "📊 Splits por KM")
            
elif aba == "⚡ Converter Pace":
    st.subheader("⚡ Converter Pace para Velocidade")
    min_km = st.number_input("Minutos por km", min_value=0)
    seg_km = st.number_input("Segundos por km", min_value=0, max_value=59)

    if st.button("Converter"):
        total_min = min_km + seg_km / 60
        kmh = round(60 / total_min, 2)

        st.markdown(f"""
            <div class="resultado">
                <strong>🚴 Velocidade:</strong> {kmh} km/h
            </div>
        """, unsafe_allow_html=True)

elif aba == "🧠 Estratégia Pace Pro":
    st.subheader("🧠 Estratégia Pace Pro")
    distancia = st.number_input("Distância da prova (km)", min_value=1)
    tempo_estimado = st.time_input("Tempo estimado (hh:mm:ss)", value=time(1, 0, 0))
    estrategia = st.selectbox("Escolha a estratégia:", ["Equilibrado", "Início mais leve", "Início mais forte"])

    if st.button("Gerar Estratégia"):
        total_min = tempo_estimado.hour * 60 + tempo_estimado.minute + tempo_estimado.second / 60
        pace_base = total_min / distancia

        dados = []
        for km in range(1, int(distancia) + 1):
            ajuste = 0
            if estrategia == "Início mais leve":
                ajuste = 0.1 * (1 - km / distancia)
            elif estrategia == "Início mais forte":
                ajuste = 0.1 * (km / distancia)

            pace_km = pace_base + ajuste if estrategia == "Início mais leve" else pace_base - ajuste if estrategia == "Início mais forte" else pace_base
            minutos = int(pace_km)
            segundos = int((pace_km - minutos) * 60)
            velocidade = round(60 / pace_km, 2)
            dados.append((str(km), f"{minutos:02d}:{segundos:02d}", f"{velocidade} km/h"))

        mostrar_tabela_splits(dados, "📊 Estratégia de Prova Pace Pro")
