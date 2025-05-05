import streamlit as st
import re
from datetime import time

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

        st.markdown(f'''
            <div class="resultado">
                <div style="display: flex; align-items: center; gap: 10px; justify-content: center;">
                    <strong>Pace:</strong> {pace_formatado}
                </div>
                <div style="display: flex; align-items: center; gap: 10px; justify-content: center; margin-top: 10px;">
                    <strong>Velocidade:</strong> {km_h} km/h
                </div>
            </div>
        ''', unsafe_allow_html=True)

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

        st.markdown(f'''
            <div class="resultado">
                <div style="display: flex; align-items: center; gap: 10px; justify-content: center;">
                    <strong>Velocidade:</strong> {km_h} km/h
                </div>
            </div>
        ''', unsafe_allow_html=True)

elif aba == "📊 Estratégia Pace Pro":
    st.subheader("🎯 Planejamento de Prova com Pace Personalizado")
    
    distancia = st.number_input("Distância da prova (km)", min_value=1, step=1)
    pace_base = st.slider("Pace base (min/km)", 3.0, 10.0, 6.0, 0.1)

    st.markdown("### Ajuste o Pace por Km")
    pace_por_km = []
    for km in range(1, int(distancia) + 1):
        pace_km = st.slider(f"{km} km", min_value=pace_base - 2, max_value=pace_base + 2, value=pace_base, step=0.1)
        minutos = int(pace_km)
        segundos = int((pace_km - minutos) * 60)
        velocidade = round(60 / pace_km, 2)
        pace_por_km.append((f"{km} km", f"{minutos:02d}:{segundos:02d}", f"{velocidade} km/h"))

    st.markdown("### 📋 Tabela Estratégica")
    st.table(pace_por_km)
