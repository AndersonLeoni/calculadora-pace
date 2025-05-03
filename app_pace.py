import streamlit as st

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

aba = st.radio("Escolha uma opção:", ["📏 Calcular Pace", "⚡ Converter Pace para km/h"], horizontal=True)

# Função para converter pace para km/h
def pace_para_kmh(minutos, segundos):
    total_minutos = minutos + segundos / 60
    return round(60 / total_minutos, 2)

if aba == "📏 Calcular Pace":
    distancia = st.number_input("Distância (km)", min_value=0.1, step=0.1)
    tempo = st.time_input("Tempo total (hh:mm:ss)")

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
                    <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
                        <path d="M12 8a1 1 0 0 1 1 1v3.586l1.707 1.707a1 1 0 0 1-1.414 1.414l-2-2A1 1 0 0 1 11 13V9a1 1 0 0 1 1-1z"/>
                        <path fill-rule="evenodd" d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm0-2a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/>
                    </svg>
                    <strong>Pace:</strong> {pace_formatado}
                </div>
                <div style="display: flex; align-items: center; gap: 10px; justify-content: center; margin-top: 10px;">
                    <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
                        <path d="M13 3a1 1 0 0 1 1 1v3.055a7.001 7.001 0 0 1 5.44 8.385 1 1 0 0 1-1.944-.43A5.002 5.002 0 0 0 14 8.127V12a1 1 0 0 1-2 0V4a1 1 0 0 1 1-1z"/>
                        <path d="M6 20a1 1 0 0 1-1-1c0-2.761 4.03-5 9-5s9 2.239 9 5a1 1 0 0 1-1 1H6z"/>
                    </svg>
                    <strong>Velocidade:</strong> {km_h} km/h
                </div>
            </div>
        ''', unsafe_allow_html=True)

elif aba == "⚡ Converter Pace para km/h":
    minutos = st.number_input("Minutos por km", min_value=0, step=1)
    segundos = st.number_input("Segundos por km", min_value=0, max_value=59, step=1)

    if st.button("Converter"):
        km_h = pace_para_kmh(minutos, segundos)

        st.markdown(f'''
            <div class="resultado">
                <div style="display: flex; align-items: center; gap: 10px; justify-content: center;">
                    <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
                        <path d="M13 3a1 1 0 0 1 1 1v3.055a7.001 7.001 0 0 1 5.44 8.385 1 1 0 0 1-1.944-.43A5.002 5.002 0 0 0 14 8.127V12a1 1 0 0 1-2 0V4a1 1 0 0 1 1-1z"/>
                        <path d="M6 20a1 1 0 0 1-1-1c0-2.761 4.03-5 9-5s9 2.239 9 5a1 1 0 0 1-1 1H6z"/>
                    </svg>
                    <strong>Velocidade:</strong> {km_h} km/h
                </div>
            </div>
        ''', unsafe_allow_html=True)
