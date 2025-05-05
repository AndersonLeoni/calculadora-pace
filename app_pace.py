import streamlit as st
from datetime import time, timedelta, datetime

st.set_page_config(page_title="Calculadora de Pace", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .resultado {
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 12px;
            margin-top: 1rem;
            font-size: 1.3rem;
            text-align: center;
        }
        input, .stButton>button {
            font-size: 1.1rem !important;
        }
        @media screen and (max-width: 768px) {
            .resultado {
                font-size: 1.5rem;
            }
            input, .stButton>button {
                font-size: 1.2rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏃 Calculadora de Pace e Velocidade")

aba = st.radio("Escolha uma opção:", ["📏 Calcular Pace", "⚡ Converter Pace", "🧠 Estratégia Pace Pro"], horizontal=True)

# Função de conversão de pace para km/h
def pace_para_kmh(minutos, segundos):
    total_min = minutos + segundos / 60
    return round(60 / total_min, 2)

# Função de exibição de splits
def exibir_splits(distancia, pace_minutos):
    st.markdown("### 📊 Splits por km")
    dados = []
    for km in range(1, int(distancia)+1):
        total_min = pace_minutos * km
        min_km = int(total_min)
        seg_km = int((total_min - min_km) * 60)
        pace_str = f"{min_km:02d}:{seg_km:02d}"
        velocidade = round(60 / pace_minutos, 2)
        dados.append((f"{km}", pace_str, f"{velocidade} km/h"))

    st.table(
        {"KM": [d[0] for d in dados],
         "Pace": [d[1] for d in dados],
         "Velocidade": [d[2] for d in dados]}
    )

if aba == "📏 Calcular Pace":
    st.subheader("📏 Calcular Pace")
    distancia = st.number_input("Distância (km)", min_value=0.1, step=0.1)
    tempo = st.time_input("Tempo total (hh:mm:ss)", value=time(0, 30, 0))

    if st.button("Calcular Pace"):
        total_minutos = tempo.hour * 60 + tempo.minute + tempo.second / 60
        pace = total_minutos / distancia
        minutos = int(pace)
        segundos = int((pace - minutos) * 60)
        pace_formatado = f"{minutos:02d}:{segundos:02d} min/km"
        km_h = round(60 / pace, 2)

        st.markdown(f'''
            <div class="resultado">
                <div style="margin-bottom:10px;"><strong>⏱️ Pace:</strong> {pace_formatado}</div>
                <div><strong>🚀 Velocidade:</strong> {km_h} km/h</div>
            </div>
        ''', unsafe_allow_html=True)

        mostrar_splits = st.toggle("👟 Ver parciais por km")
        if mostrar_splits:
            exibir_splits(distancia, pace)

elif aba == "⚡ Converter Pace":
    st.subheader("⚡ Converter Pace para km/h")
    min_km = st.number_input("Minutos por km", min_value=0)
    seg_km = st.number_input("Segundos por km", min_value=0, max_value=59)

    if st.button("Converter"):
        kmh = pace_para_kmh(min_km, seg_km)
        st.markdown(f'''
            <div class="resultado">
                <strong>🚴 Velocidade:</strong> {kmh} km/h
            </div>
        ''', unsafe_allow_html=True)

elif aba == "🧠 Estratégia Pace Pro":
    st.subheader("🧠 Estratégia Pace Pro")
    distancia = st.number_input("Distância da prova (km)", min_value=1)
    tempo_estimado = st.time_input("Tempo estimado (hh:mm:ss)", value=time(1, 0, 0))
    estrategia = st.selectbox("Escolha a estratégia:", ["Equilibrado", "Início mais leve", "Início mais forte"])

    if st.button("Gerar Estratégia Pace Pro"):
        total_min = tempo_estimado.hour * 60 + tempo_estimado.minute + tempo_estimado.second / 60
        pace_base = total_min / distancia

        splits = []
        for km in range(1, distancia + 1):
            ajuste = 0
            if estrategia == "Início mais leve":
                ajuste = 0.1 * (1 - km / distancia)
            elif estrategia == "Início mais forte":
                ajuste = 0.1 * (km / distancia)

            pace_km = pace_base + ajuste if estrategia == "Início mais leve" else pace_base - ajuste if estrategia == "Início mais forte" else pace_base
            min_km = int(pace_km)
            seg_km = int((pace_km - min_km) * 60)
            pace_str = f"{min_km:02d}:{seg_km:02d}"
            velocidade = round(60 / pace_km, 2)
            splits.append((f"{km}", pace_str, f"{velocidade} km/h"))

        st.markdown("### 📊 Estratégia de Prova (Pace Pro)")
        st.table(
            {"KM": [d[0] for d in splits],
             "Pace": [d[1] for d in splits],
             "Velocidade": [d[2] for d in splits]}
        )
