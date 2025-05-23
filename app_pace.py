import streamlit as st
from datetime import datetime, timedelta

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
        input[type="time"]::-webkit-calendar-picker-indicator {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏃 Calculadora de Pace e Estratégia de Prova")

aba = st.radio("Escolha uma opção:", ["📏 Calcular Pace", "⚡ Converter Pace", "🏁 Pace Pro"], horizontal=True)

def calcular_splits(distancia, pace_min_km):
    dados = []
    for km in range(1, int(distancia) + 1):
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
    tempo = st.text_input("Tempo total (hh:mm:ss)", value="00:30:00")

    if "pace_calculado" not in st.session_state:
        st.session_state.pace_calculado = False

    if st.button("Calcular Pace"):
        try:
            h, m, s = map(int, tempo.split(":"))
            total_minutos = h * 60 + m + s / 60
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
        except:
            st.error("Formato de tempo inválido. Use hh:mm:ss.")

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

elif aba == "🏁 Pace Pro":
    st.subheader("🏁 Estratégia Pace Pro")

    distancia_pp = st.number_input("Distância da prova (km)", min_value=1.0, step=0.1, format="%.1f")
    tempo_digitado = st.text_input("Tempo previsto (hh:mm:ss)", value="01:00:00")
    estrategia = st.radio("Escolha a estratégia:", ["⚖️ Ritmo equilibrado", "🎯 Início mais leve", "🔥 Início mais forte"])

    gerar = st.button("Gerar Estratégia Pace Pro")

    if gerar:
        try:
            h, m, s = map(int, tempo_digitado.split(":"))
            total_minutos = h * 60 + m + s / 60
            pace_medio = total_minutos / distancia_pp

            splits = []
            fator = 0.03  # 3% de variação no ritmo

            for km in range(1, int(distancia_pp) + 1):
                ajuste = (km - 1) / (distancia_pp - 1) if distancia_pp > 1 else 0

                if estrategia == "⚖️ Ritmo equilibrado":
                    pace_km = pace_medio
                elif estrategia == "🎯 Início mais leve":
                    pace_km = pace_medio * (1 + fator * (1 - ajuste))
                else:  # início mais forte
                    pace_km = pace_medio * (1 - fator * (1 - ajuste))

                minutos = int(pace_km)
                segundos = int((pace_km - minutos) * 60)
                velocidade = round(60 / pace_km, 2)
                splits.append((str(km), f"{minutos:02d}:{segundos:02d}", f"{velocidade} km/h"))

            mostrar_tabela_splits(splits, "📈 Estratégia Pace Pro")
        except:
            st.error("Formato de tempo inválido. Use hh:mm:ss.")
